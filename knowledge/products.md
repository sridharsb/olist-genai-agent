# 🇧🇷 Olist E-commerce Knowledge Base

This document provides contextual knowledge to enrich analytical answers from the
Brazilian Olist e-commerce dataset (2016–2018).  
It does NOT change query results — it only improves explanations and insights.

---

## 📦 About the Olist Dataset

Olist is a Brazilian marketplace that connects small and medium sellers to
large online marketplaces.  
The dataset represents real-world e-commerce operations, including:

- Orders placed between **September 2016 and September 2018**
- ~100,000 anonymized orders
- Customers across all Brazilian states
- Multiple sellers per order
- Multiple payment methods per order

The dataset is commonly used to study:
- Revenue distribution
- Category performance
- Logistics efficiency
- Customer behavior
- Seller dynamics

---

## 💰 Revenue Definition (Important)

In Olist:
- **Revenue = SUM(payments.payment_value)**
- `price` represents item price
- `freight_value` represents shipping cost
- Payment value may include:
  - Installments
  - Discounts
  - Multiple payment methods per order

Revenue should **never** be calculated by multiplying price or quantity.

---

## 🏷️ Product Categories – Business Meaning

### beleza_saude
Beauty and health products such as cosmetics, skincare, personal hygiene,
and wellness items.  
Typically high-volume with repeat purchases.

### cama_mesa_banho
Home essentials including bedsheets, towels, pillows, and linens.
Often seasonal and promotion-driven.

### moveis_decoracao
Furniture and home décor products like shelves, lighting, and decorative items.
Lower order frequency but higher ticket size.

### moveis_escritorio
Office furniture such as desks, office chairs, and storage units.
Sales often driven by small businesses and home offices.

### eletrodomesticos
Large home appliances like refrigerators, washing machines, and ovens.
High-value items with lower order counts.

### eletrodomesticos_2
Smaller appliances such as blenders, coffee machines, and microwaves.
Higher frequency compared to large appliances.

### informatica_acessorios
Computer accessories including keyboards, mice, cables, and peripherals.
High demand due to digitalization trends.

### telefonia
Mobile phones and accessories such as chargers, cases, and earphones.
Fast-moving category with frequent model changes.

### brinquedos
Children’s toys and games.
Strong seasonality around holidays and gifting periods.

### livros_interesse_geral
General-interest books, including educational and leisure reading.
Moderate volume, often price-sensitive.

### fashion_bolsas_e_acessorios
Bags, wallets, belts, and fashion accessories.
Style-driven purchases with moderate price points.

### fashion_calcados
Shoes and footwear.
Highly competitive category with size and fit considerations.

### fashion_roupa_feminina
Women’s clothing.
High SKU variety and trend-driven sales.

### fashion_roupa_masculina
Men’s clothing.
Lower variety but more stable demand.

### fashion_underwear_e_moda_praia
Underwear and swimwear.
Seasonal, influenced by climate and vacations.

### esporte_lazer
Sports equipment and leisure products.
Sales influenced by fitness trends and seasons.

### pet_shop
Pet food, toys, and accessories.
Recurring demand and high customer loyalty.

### papelaria
Office supplies, stationery, and school materials.
Seasonal spikes during school periods.

### alimentos
Packaged food and groceries.
Lower margins but consistent demand.

### bebidas
Non-alcoholic beverages and related products.
Often impulse-driven purchases.

### seguros_e_servicos
Digital services and insurance-related products.
Typically very low revenue compared to physical goods.
Often appears as the **lowest-revenue category**.

---

## 🚚 Logistics & Delivery Context

- Orders include estimated and actual delivery dates
- Delivery delays can occur due to:
  - Long-distance shipping
  - Holidays
  - National trucker strikes (notably in 2018)
- Freight costs vary significantly by region

Delivery performance is a key driver of customer reviews.

---

## ⭐ Customer Reviews

- Reviews range from 1 to 5 stars
- Influenced by:
  - Delivery speed
  - Product quality
  - Packaging condition
- Late deliveries often result in lower ratings

---

## 🧠 How to Interpret “Most Sold” vs “Highest Revenue”

- **Most sold** → highest number of order items
- **Highest revenue** → highest total payment value
- A category can be:
  - High volume but low revenue (cheap items)
  - Low volume but high revenue (expensive items)

Always clarify which metric is being used.

---

## 📊 Common Analytical Questions Supported

- Highest / lowest revenue category
- Average revenue per category
- Revenue trends over time (2016–2018)
- Product-level revenue analysis
- Most / least sold categories
- Category distribution across years

---

## ⚠️ Dataset Limitations

- No data after 2018
- No real-time inventory
- No product descriptions beyond category
- Prices may not reflect inflation

Insights should be interpreted as **historical trends**, not current market state.

---

## 🤖 How This Knowledge Is Used

This knowledge is:
- Used only for explanations and insights
- Retrieved via RAG
- Never used to generate SQL
- Never overrides actual query results

It exists to make answers more human, contextual, and business-friendly.
