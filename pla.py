
import mysql.connector
from fatsecret import Fatsecret
CONSUMER_KEY = '7d84a387593e4412ae6646facc9ddc3f'
CONSUMER_SECRET = '246887260e314652b1fec29f8412ad05'
fs = Fatsecret(CONSUMER_KEY, CONSUMER_SECRET)

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="duan6"
)
cursor = db_connection.cursor()



# Lấy dữ liệu của công thức với ID là 20
recipe_id = 61035855
recipe_data = fs.recipe_get(recipe_id=recipe_id)

# Kiểm tra xem công thức có tồn tại không
if recipe_data:
    # Lặp qua từng thành phần trong công thức
    for ingredient in recipe_data['ingredients']['ingredient']:
        found = False
        food_id = ingredient['food_id']
        measurement_description = ingredient['measurement_description']
        
        # Truy vấn thông tin dinh dưỡng từ Fatsecret API
        food_info = fs.food_get(food_id)
        
        if food_info:
            s=food_info['servings']['serving']
            # Lặp qua các loại khẩu phần của thực phẩm để tìm thông tin về khẩu phần cụ thể
            if len(s) > 12:
                servings = [food_info['servings']['serving']]
            else:
                servings  = food_info['servings']['serving']                
            for p in servings:
                if p['measurement_description'] == measurement_description:
                    # Thêm thông tin vào cơ sở dữ liệu
                    sql = """INSERT INTO ingredients (id, category, name, calcium, calories, carbohydrate, cholesterol, fiber, iron, fat, monounsaturated_fat, polyunsaturated_fat, saturated_fat, potassium, protein, sodium, sugar, vitamin_a, vitamin_c) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    for i in  ['calcium', 'calories', 'carbohydrate', 'cholesterol', 'fiber', 'iron', 'fat', 'monounsaturated_fat', 'polyunsaturated_fat', 'saturated_fat', 'potassium', 'protein', 'sodium', 'sugar', 'vitamin_a', 'vitamin_c']:
                        if i not in p:
                            p[i] = None
                    val = (food_info['food_id'],None, food_info['food_name'], p['calcium'], p['calories'], p['carbohydrate'], p['cholesterol'], p['fiber'], p['iron'], p['fat'], p['monounsaturated_fat'], p['polyunsaturated_fat'], p['saturated_fat'], p['potassium'], p['protein'], p['sodium'], p['sugar'], p['vitamin_a'], p['vitamin_c'])
                    cursor.execute(sql, val)
                    db_connection.commit()
                    found = True  # Đánh dấu là đã tìm thấy khẩu phần phù hợp
                    break
            if not found:
                print("Not found")
                break
    all_directions = ""
    for direction in recipe_data.get('directions', {}).get('direction', []):
        direction_number = direction.get('direction_number', None)
        direction_description = direction.get('direction_description', None)
        all_directions += f"{direction_number}. {direction_description}\n"
    recipe_info = recipe_data


    a=['Breakfast','Lunch','Dinner']
    b=['Appetizer','Main Dish','Side Dish','Dessert']
    c=['Baked','Salad and Salad Dressing','Sauce and Condiment','Snack','Beverage','Soup','Other']

    d=e=f=None
    print(recipe_info['recipe_types']['recipe_type'])
    for item in recipe_info['recipe_types']['recipe_type']:
        if item in a:
            d = item
        elif item in b:
            e = item
        elif item in c:
            f = item
    for i in ['recipe_id', 'recipe_name', 'recipe_description', 'preparation_time_min', 'cooking_time_min', 'number_of_servings']:
        if i not in recipe_info:
            recipe_info[i] = None
    if 'recipe_images' not in recipe_info:
        sql_recipe = """INSERT INTO recipes (id,name, description, preparation_time_min,cooking_time_min,  number_of_servings, directions, meal_type_1,meal_type_2,meal_type_3) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"""
        val_recipe = (recipe_info['recipe_id'], recipe_info['recipe_name'], recipe_info['recipe_description'], recipe_info['preparation_time_min'], recipe_info['cooking_time_min'], recipe_info['number_of_servings'], all_directions,d,e,f)
    else:
        sql_recipe = """INSERT INTO recipes (id,name, description, image_url, preparation_time_min,cooking_time_min,  number_of_servings, directions, meal_type_1,meal_type_2,meal_type_3) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
        val_recipe = (recipe_info['recipe_id'], recipe_info['recipe_name'], recipe_info['recipe_description'], recipe_info['recipe_images']['recipe_image'], recipe_info['preparation_time_min'], recipe_info['cooking_time_min'], recipe_info['number_of_servings'], all_directions,d,e,f)
    cursor.execute(sql_recipe, val_recipe)
    db_connection.commit()


else:
    print("Recipe not found.")



# Đóng kết nối
cursor.close()
db_connection.close()




















'''


from fatsecret import Fatsecret
import mysql.connector

# FatSecret API credentials
CONSUMER_KEY = '7d84a387593e4412ae6646facc9ddc3f'
CONSUMER_SECRET = '246887260e314652b1fec29f8412ad05'

# MySQL database credentials
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'mysql'
DB_DATABASE = 'duan2'

# Create Fatsecret object
fs = Fatsecret(CONSUMER_KEY, CONSUMER_SECRET)

# Connect to MySQL database
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = connection.cursor()

# Function to insert data into MongolianBBQ table
def insert_into_mongolian_bbq(recipe_data):
    all_directions = ""
    # Lặp qua mỗi hướng dẫn trong danh sách
    for direction in recipe_data.get('directions', {}).get('direction', []):
        direction_number = direction.get('direction_number', None)
        direction_description = direction.get('direction_description', None)
        all_directions += f"{direction_number}. {direction_description}\n"
        

        # Thực hiện INSERT INTO với các giá trị này
    insert_query = """
        INSERT INTO RecipeDirections (
            recipe_id, direction_number, direction_description
        ) VALUES (
            %s, %s, %s
        )
    """
        
        # Tuple chứa giá trị để chèn
    du_lieu_mon_an = (
        recipe_data.get('recipe_id', None),
        direction_number,
        all_directions,
    )

        # Thực hiện câu lệnh INSERT INTO
    cursor.execute(insert_query, du_lieu_mon_an)
    print(f"Thêm dữ liệu cho {recipe_data.get('recipe_id', None)} hướng dẫn số {direction_number} thành công.")

# Function to get recipe data based on name starting with 'a'
def lay_du_lieu_cac_cong_thuc_theo_tieu_chi():
    # Hàm recipes_search trả về danh sách các công thức dựa trên tiêu chí tìm kiếm
    #select_query = "SELECT recipe_id FROM recipe1"

    # Execute the query
    #cursor.execute(select_query)

    # Fetch all the rows and convert them to a list
    #rows = cursor.fetchall()
    #ket_qua_tim_kiem = [row[0] for row in rows]
    ket_qua_tim_kiem=[20]
    # Gọi hàm chèn dữ liệu vào MySQL cho từng công thức
    for p in ket_qua_tim_kiem:
        insert_into_mongolian_bbq(fs.recipe_get(p))

# Set FOREIGN_KEY_CHECKS to 0 before making changes
cursor.execute("SET FOREIGN_KEY_CHECKS=0")

# Gọi hàm để lấy và chèn dữ liệu
lay_du_lieu_cac_cong_thuc_theo_tieu_chi()
cursor.execute("SET FOREIGN_KEY_CHECKS=1")

# Commit the changes and close the connection
connection.commit()
connection.close()
 '''