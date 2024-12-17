import yaml
from flask import Flask, render_template, request
from ram_db import CompList, sort_by_field
from categories import SortElement
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)




comp_list = CompList()
comp_list.add_product('Electronics', 'Laptop', 999.99, True)
comp_list.add_product('Electronics', 'Smartphone', 499.99, False)
comp_list.add_product('Furniture', 'Chair', 59.99, True)
list = comp_list.comp

@app.route('/')
def hello_world():
    """
    Main page to display the product list
    ---
    parameters:
      - name: sort
        in: query
        type: string
        description: Field to sort by
      - name: min_price
        in: query
        type: string
        description: Minimum price filter
      - name: max_price
        in: query
        type: string
        description: Maximum price filter
      - name: desc_asc
        in: query
        type: string
        description: Sort order (desc/asc)
    responses:
      200:
        description: A list of products
    """
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    desc_asc = request.args.get('desc_asc')

    if not sort:
        return render_template('index.html', list=list, sort=SortElement, filter_selected={})

    sort = sort.lower()

    filter_selected = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'desc_asc': desc_asc
    }

    list_result = []
    if isinstance(min_price, str):
        list_result.append(comp_list.get_min_price_record())
    if isinstance(max_price, str):
        list_result.append(comp_list.get_max_price_record())

    if not list_result:
        list_result = sort_by_field(list, sort, desc_asc)
    else:
        list_result = sort_by_field(list_result, sort, desc_asc)

    return render_template('index.html', list=list_result, sort=SortElement, filter_selected=filter_selected)


@app.route('/add', methods=['POST'])
def add_product():
    """
    Add a new product to the list
    ---
    parameters:
      - name: category
        in: formData
        type: string
        required: true
        description: Category of the product
      - name: name
        in: formData
        type: string
        required: true
        description: Name of the product
      - name: price
        in: formData
        type: number
        required: true
        description: Price of the product
      - name: present
        in: formData
        type: boolean
        required: true
        description: Whether the product is present
    responses:
      200:
        description: Product added successfully
    """
    category = request.form['category']
    name = request.form['name']
    price = float(request.form['price'])
    present = request.form.get('present') == 'on'

    comp_list.add_product(category, name, price, present)
    return render_template('index.html', list=list, sort=SortElement, filter_selected={})


@app.route('/remove', methods=['GET'])
def remove_product():
    """
    Remove a product from the list
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: true
        description: ID of the product to remove
    responses:
      200:
        description: Product removed successfully
    """
    _id = int(request.args.get('id'))
    comp_list.remove_product(_id)
    return render_template('index.html', list=list, sort=SortElement, filter_selected={})


@app.route('/update', methods=['POST'])
def update():
    """
    Update a product in the list
    ---
    parameters:
      - name: id
        in: body
        schema:
          id: ProductUpdateRequest
          required:
            - id
            - category
            - name
            - price
            - present
          properties:
            id:
              type: integer
              description: ID of the product to update
            category:
              type: string
              description: New category of the product
            name:
              type: string
              description: New name of the product
            price:
              type: number
              description: New price of the product
            present:
              type: boolean
              description: New present status of the product
    responses:
      200:
        description: Product updated successfully
    """
    data = request.get_json()
    _id = int(data['id'])
    category = data['category']
    name = data['name']
    price = float(data['price'])
    present = data['present']
    comp_list.update_product(_id, category, name, price, present)
    return render_template('index.html', list=list, sort=SortElement, filter_selected={})


if __name__ == '__main__':
    app.run()