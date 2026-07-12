# Slice Matic Post Development Discussion

**Date:** 2026-11-07 | **Type:** Workshop

## What We Covered

- Slice Matic
  - Think in terms of the user
  - style it from the MVP
  - think of design at MVP stage
  - Which features can be classified as primary or secondary
  - Would we be putting it all in one git hub repo or keep it in a separate repo
  - Our primary services should not be affected when secondary services change
  - Have different services
  - Follow micro services architecture
  - Group dependant actions
  - Always have a coordinator below our APIs
  - Below coordinators we need specialists
  - Features (5-6 Features)
    - view the menu
    - choose base
    - choose pizza
    - choose topping
    - select quantity
    - calculate price
    - place the order

- HLD
  - Overview of a project
  - Core Services
    - Menu
    - Orders
    - Analytics
    - Recommendation reciever

  - DB Service
    - Database (Supabase)
  - AI recommendation

- Generic ideas on how to design a system
  - start with real user action
  - expand the hidden flow. Be as technical as possible
  - split the work that changes for different reasons
  - group replated work
  - hide replaceble tech

- Functions
  - Menu
    - Recieve the menu request
    - read the active bases, toppings, pizza from the DB
    - return the active menu
  - Order
    - Actions of the user
      - select the menu
      - check the cart
      - gets recommendations
      - searches
      - place the order
  - Admin View
    - Analytics Query
      - counting orders
      - total sales for the day
      - stock analysis

- LLD of Menu API
  - Access the menu
  - Menu Repository can be reused in Order API

- LLD of Recommendation reciever
  - Reuse Customer Repository

- LLD of Order API
  - hidden flow
    - recieve the item ids
    - validate the request
    - read the item prices
    - calculate the total
    - get the customer details using customer id
    - create a customer if required
    - save the order in the DB
    - return confirmation
  - split the work that changes for different reasons
  - Have a coordinator which will call the below specialists
    - Menu Repository
      - recieve the item ids
      - validate the request
      - read the item prices
    - Pricing policy
      - calculate the total
    - Customer Repository
      - get the customer details using customer id
      - create a customer if required
    - order repository
      - save the order in the DB
      - return confirmation

- 3 layer architecture
  - controller
  - manager

## What I Built / Key Takeaways

-

## Insights & Opinions

-

## Open Questions

- Architecture
  ![Architecture](./Screenshot%202026-07-11%20193257.png)

```mermaid
---
config:
  theme: redux
  layout: elk
---
flowchart TB
 subgraph s1["Frontend"]
        n5["Menu"]
        n6["Orders"]
        n7["Admin"]
        n8["AI Recommendation"]
  end
 subgraph s2["API Layer"]
        n10["/api/menu"]
        n11["/api/oders"]
        n12["/api/admin"]
        n13["/api/admin"]
  end
 subgraph s3["Coordinators"]
        n14["get meunu usecase"]
        n15["place order usecase"]
        n16["analytics usecase"]
        n17["recommendation usecase"]
  end
 subgraph s4["Specialists"]
        n18["menu repo"]
        n20["customer repo"]
        n21["order repo"]
        n19["pricing policy"]
        n22["analytics repo"]
        n23["recommendation repo"]
  end
    n5 --> n10
    n10 --> n14
    n14 --> n18
    n18 --> n24["Supabase"]
    n6 --> n11
    n11 --> n15
    n15 --> n18 & n20 & n21 & n19
    n7 --> n12
    n12 --> n16
    n16 --> n21 & n22
    n8 --> n13
    n13 --> n17
    n17 --> n23
    n23 --> n25["FastAPI Recommendation"]
    n25 --> n26["Recommendation"]
    n19 --> n24
    n20 --> n24
    n21 --> n24
    n22 --> n24

    n5@{ shape: rounded}
    n6@{ shape: rounded}
    n7@{ shape: rounded}
    n8@{ shape: rounded}
    n10@{ shape: rounded}
    n11@{ shape: rounded}
    n12@{ shape: rounded}
    n13@{ shape: rounded}
    n14@{ shape: rounded}
    n15@{ shape: rounded}
    n16@{ shape: rounded}
    n17@{ shape: rounded}
    n18@{ shape: rounded}
    n20@{ shape: rounded}
    n21@{ shape: rounded}
    n19@{ shape: rounded}
    n22@{ shape: rounded}
    n23@{ shape: rounded}
    n24@{ shape: rounded}
    n25@{ shape: rounded}
    n26@{ shape: rounded}
```
