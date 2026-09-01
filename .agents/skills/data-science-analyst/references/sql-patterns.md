# SQL Patterns

Templates SQL para analytics, validação e métricas. Ajuste sintaxe para o dialeto do banco: BigQuery, Snowflake, Postgres, Redshift, DuckDB etc.

## Query structure

```sql
-- Purpose:
-- Grain:
-- Time window:
-- Filters:
-- Metric definition:
-- Known caveats:

WITH source AS (
    SELECT
        user_id,
        event_time,
        event_name,
        amount
    FROM schema.events
    WHERE event_time >= DATE '2026-01-01'
      AND event_time <  DATE '2026-02-01'
),

validated AS (
    SELECT
        *
    FROM source
    WHERE user_id IS NOT NULL
)

SELECT
    COUNT(*) AS events,
    COUNT(DISTINCT user_id) AS users
FROM validated;
```

## Row count validation

```sql
WITH base AS (
    SELECT * FROM schema.table_a
),

joined AS (
    SELECT
        a.*,
        b.attribute
    FROM base a
    LEFT JOIN schema.table_b b
        ON a.id = b.id
)

SELECT 'base' AS step, COUNT(*) AS rows FROM base
UNION ALL
SELECT 'joined' AS step, COUNT(*) AS rows FROM joined;
```

## Duplicate key check

```sql
SELECT
    id,
    COUNT(*) AS row_count
FROM schema.table_name
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY row_count DESC;
```

## Funnel template

```sql
WITH events AS (
    SELECT
        user_id,
        event_name,
        event_time
    FROM schema.events
    WHERE event_time >= DATE '2026-01-01'
      AND event_time <  DATE '2026-02-01'
),

steps AS (
    SELECT
        user_id,
        MIN(CASE WHEN event_name = 'visited' THEN event_time END) AS visited_at,
        MIN(CASE WHEN event_name = 'signed_up' THEN event_time END) AS signed_up_at,
        MIN(CASE WHEN event_name = 'purchased' THEN event_time END) AS purchased_at
    FROM events
    GROUP BY user_id
),

ordered_steps AS (
    SELECT
        user_id,
        visited_at,
        CASE WHEN signed_up_at > visited_at THEN signed_up_at END AS signed_up_at,
        CASE WHEN purchased_at > signed_up_at THEN purchased_at END AS purchased_at
    FROM steps
)

SELECT
    COUNT(*) AS users_entered,
    COUNT(signed_up_at) AS users_signed_up,
    COUNT(purchased_at) AS users_purchased,
    1.0 * COUNT(signed_up_at) / NULLIF(COUNT(*), 0) AS signup_rate,
    1.0 * COUNT(purchased_at) / NULLIF(COUNT(signed_up_at), 0) AS purchase_after_signup_rate
FROM ordered_steps
WHERE visited_at IS NOT NULL;
```

## Cohort retention template

```sql
WITH activity AS (
    SELECT
        user_id,
        DATE_TRUNC('week', event_time) AS activity_week
    FROM schema.events
    WHERE event_name = 'active'
    GROUP BY 1, 2
),

cohorts AS (
    SELECT
        user_id,
        MIN(activity_week) AS cohort_week
    FROM activity
    GROUP BY user_id
),

retention AS (
    SELECT
        c.cohort_week,
        a.activity_week,
        DATEDIFF('week', c.cohort_week, a.activity_week) AS week_number,
        COUNT(DISTINCT a.user_id) AS active_users
    FROM cohorts c
    JOIN activity a
      ON c.user_id = a.user_id
     AND a.activity_week >= c.cohort_week
    GROUP BY 1, 2, 3
),

cohort_sizes AS (
    SELECT
        cohort_week,
        COUNT(DISTINCT user_id) AS cohort_users
    FROM cohorts
    GROUP BY cohort_week
)

SELECT
    r.cohort_week,
    r.week_number,
    r.active_users,
    s.cohort_users,
    1.0 * r.active_users / NULLIF(s.cohort_users, 0) AS retention_rate
FROM retention r
JOIN cohort_sizes s USING (cohort_week)
ORDER BY r.cohort_week, r.week_number;
```

## Revenue metric template

```sql
WITH orders AS (
    SELECT
        order_id,
        user_id,
        created_at,
        amount,
        status
    FROM schema.orders
    WHERE created_at >= DATE '2026-01-01'
      AND created_at <  DATE '2026-02-01'
      AND status NOT IN ('cancelled', 'refunded')
)

SELECT
    DATE_TRUNC('day', created_at) AS order_day,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT user_id) AS customers,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_order_value
FROM orders
GROUP BY 1
ORDER BY 1;
```

## Sample ratio mismatch for A/B tests

```sql
WITH assignments AS (
    SELECT
        variant,
        COUNT(DISTINCT user_id) AS users
    FROM experiment.assignments
    WHERE experiment_id = 'experiment_name'
    GROUP BY variant
)

SELECT
    variant,
    users,
    1.0 * users / SUM(users) OVER () AS allocation_share
FROM assignments;
```

## Timezone warning

Always state whether timestamps are stored as UTC or local time. Prefer explicit conversion before date truncation:

```sql
DATE_TRUNC('day', event_time AT TIME ZONE 'America/Sao_Paulo') AS event_day_local
```
