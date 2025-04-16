class OrderProcessor:
    def __init__(self, menu_db, llm_parser):
        self.menu_db = menu_db
        self.llm_parser = llm_parser

    def process_order(self, text):
        print("\n🧠 Parsing order using LLM...")
        orders = self.llm_parser.parse(text)

        if not orders:
            print("❌ No valid items found in transcription.")
            return

        menu_items = {name.lower(): (name, price, stock) for name, price, stock in self.menu_db.get_all_items()}

        total = 0
        print("\n🧾 Order Summary:")
        for order in orders:
            item = order['item'].lower()
            qty = order.get('quantity', 1)
            if item in menu_items:
                name, price, stock = menu_items[item]
                if stock >= qty:
                    print(f"- {name} x{qty}: ${price * qty:.2f}")
                    total += price * qty
                    self.menu_db.update_stock(name, stock - qty)
                else:
                    print(f"❗ Not enough stock for {name}")
            else:
                print(f"❓ Unknown item: {order['item']}")
        print(f"💰 Total: ${total:.2f}")