from sqlalchemy.orm import Session
from database import engine
from db_models import Product


products = [
    Product(
        product_name="Snitch Textured Cuban Shirt XL",
        price=1299,
        description='SNITCH is an Indian fast-fashion D2C menswear brand founded in 2019 by Siddharth Dungarwal in Bengaluru. It pivoted from B2B to D2C in 2020, focusing on trendy, affordable apparel for Gen Z and millennials. After securing an "all-shark" deal on Shark Tank India, it grew rapidly. Operating an omnichannel model with over 100 offline stores, a 21-day design-to-delivery cycle, and recent ₹340 crore Series B funding, SNITCH tracks a ₹900 crore revenue run rate for FY26.'
    ),
    Product(
        product_name="RJ45 Cable",
        price=599,
        description='RJ45 is the standard type of connector used for Ethernet cables to connect computers, routers, and switches in a local network (LAN) [0.1, 0.2]. The term is commonly used to describe the entire networking cable itself.'
    ),
    Product(
        product_name="Infuser Water Bottle",
        price=399,
        description='Infuser water bottles allow you to naturally flavour your water by placing fruits, vegetables, or herbs into a built-in basket or chamber, keeping pulp and seeds separated while releasing natural vitamins and minerals.'
    ),
    Product(
        product_name="Minimalist Hyaluric Acid Serum",
        price=799,
        description='Minimalist 2% Hyaluronic Acid + PGA Face Serum is a highly popular, fragrance-free hydrating booster designed to target skin tightness, dehydration, and early fine lines. It is carefully formulated to suit all skin types, including sensitive and acne-prone skin.'
    ),
    Product(
        product_name="Usha Air MAXX 1700 RPM",
        price=1899,
        description='Usha is one of India’s most trusted home appliance brands, widely recognized for its durable, high-performance ceiling, table, and pedestal fans. Modern Usha models focus heavily on energy-efficient BLDC motors, ultra-high-speed air delivery, and dust-resistant metallic finishes.'
    )
]

with Session(engine) as session:
    session.add_all(products)
    session.commit()
    print("5 products added")