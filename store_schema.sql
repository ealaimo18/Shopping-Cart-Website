DROP TABLE IF EXISTS user ;
CREATE TABLE user (
  user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  name       varchar(50) not null,
  username   varchar(50) not null,
  password   varchar(50) not null
  -- primary key (user_id)
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
  category_name varchar(50) not null,
  primary key(category_name)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  product_id            int(9) not null,
  product_name          varchar(50) not null,
  product_category_name varchar(50) not null,
  product_price         int(9) not null,
  inventory             int(9) not null,
  primary key (product_id),
  foreign key (product_category_name) references category(category_name)
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id      int(9) not null,
  order_user    int(9) not null,
  order_date    text not null,
  order_product int(9) not null,
  quantity      int(9) not null,
  -- primary key(order_id),
  foreign key (order_user) references user(user_id)
  foreign key (order_product) references product(product_id)
);



INSERT INTO user (user_id, name, username, password) VALUES
  (1,'test', 'testuser', 'testpass');
INSERT INTO user (user_id, name, username, password)VALUES 
  (2,'manue alaimo', 'malaimo', 'pass');
INSERT INTO user (user_id, name, username, password)VALUES 
  (3,'zoë robertson', 'zenmaster', 'pass');

INSERT INTO category VALUES ('cereal');
INSERT INTO category VALUES ('milk');
INSERT INTO category VALUES ('bowls');
INSERT INTO category VALUES ('spoons');

INSERT INTO product VALUES 
  (100000001, 'cheerios', 'cereal', 3.99, 100);
INSERT INTO product VALUES 
  (100000002, 'honey bunches of oats', 'cereal', 3.99, 100);
INSERT INTO product VALUES 
  (100000003, 'froot loops', 'cereal', 3.99, 100);
INSERT INTO product VALUES 
  (100000004, 'lucky charms', 'cereal', 3.99, 100);
  
INSERT INTO product VALUES 
  (200000001, 'cow milk', 'milk', 2.50, 100);
INSERT INTO product VALUES 
  (200000002, 'almond milk', 'milk', 3.99, 100);
INSERT INTO product VALUES 
  (200000003, 'oat milk', 'milk', 4.99, 100);
INSERT INTO product VALUES 
  (200000004, 'strawberry milk', 'milk', 2.99, 100);

INSERT INTO product VALUES 
  (300000001, 'cereal killer bowl', 'bowls', 7.99, 100);
INSERT INTO product VALUES 
  (300000002, 'i cerealsly love you bowl', 'bowls', 7.99, 100);
INSERT INTO product VALUES 
  (300000003, 'tie dye bowl', 'bowls', 7.99, 100);
INSERT INTO product VALUES 
  (300000004, 'dino bowl', 'bowls', 7.99, 100);

INSERT INTO product VALUES 
  (400000001, 'metallic spoon', 'spoons', 2.99, 100);
INSERT INTO product VALUES 
  (400000002, 'black matte spoon', 'spoons', 2.99, 100);
INSERT INTO product VALUES 
  (400000003, 'straw spoon', 'spoons', 2.99, 100);
INSERT INTO product VALUES 
  (400000004, 'golden spoon', 'spoons', 2.99, 100);



  
