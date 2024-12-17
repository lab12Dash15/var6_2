def sort_by_field(array, field, order='asc'):
    if field not in ['id', 'category', 'name', 'price', 'present']:
        raise ValueError("Invalid field")

    sorted_list = sorted(array, key=lambda x: x[field], reverse=(order == 'desc'))
    return sorted_list


class CompList:
    def __init__(self):
        self.comp = []

    def add_product(self, category, name, price, present):
        if self.comp:
            new_id = max(int(item['id']) for item in self.comp) + 1
        else:
            new_id = 1
        product = {
            'id': new_id,
            'category': category,
            'name': name,
            'price': price,
            'present': present
        }
        self.comp.append(product)

    def remove_product(self, _id):
        for product in self.comp:
            if product['id'] == _id:
                self.comp.remove(product)
                return True
        return False

    def update_product(self, _id, category, name, price, present):
        for product in self.comp:
            if product['id'] == _id:
                product['category'] = category
                product['name'] = name
                product['price'] = price
                product['present'] = present
                return True
        return False

    def get_min_price_record(self):
        if not self.comp:
            return None
        return min(self.comp, key=lambda x: x['price'])

    def get_max_price_record(self):
        if not self.comp:
            return None
        return max(self.comp, key=lambda x: x['price'])