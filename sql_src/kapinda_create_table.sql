-- Drop database ODS if exists
DROP DATABASE IF EXISTS kapinda;
CREATE DATABASE kapinda;
USE kapinda;

-- Delete the schemas

DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Adres;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Cart;
DROP TABLE IF EXISTS Delivery;
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS Rating;

-- Create the schemas

CREATE TABLE Customer (
    Customer_ID     CHAR(6),
    Ad      VARCHAR(20),
    Soyad       VARCHAR(20),
    Email           VARCHAR(40),
    Sifre        VARCHAR(20),
    Telefon_no          CHAR(10),
    CONSTRAINT Customer_ID_FMT CHECK (Customer_ID REGEXP "^C[0-9]{5}$"),
	CONSTRAINT Customer_Email_FMT CHECK (Email REGEXP "^[a-zA-Z0-9_]{1,20}\.?[a-zA-Z0-9_]{0,5}@[a-z]{1,7}(\.com|\.ac\.in)$"),
    CONSTRAINT Customer_Sifre_FMT CHECK (Sifre REGEXP "^[a-zA-Z0-9@#&!\$]{8,20}$"),
    CONSTRAINT Customer_Telefon_no_FMT CHECK (Telefon_no REGEXP "^[0-9]{10}$"),
    CONSTRAINT Customer_PK PRIMARY KEY (Customer_ID)
);

CREATE TABLE City (
 City_ID int NOT NULL AUTO_INCREMENT,
 City_name varchar(30) NOT NULL,
 PRIMARY KEY (City_ID)
);

CREATE TABLE Adres (
    Customer_ID     CHAR(6),
    Adres_ID      CHAR(6),
    Pincode         CHAR(6),
    Street          VARCHAR(20),
    Landmark        VARCHAR(20),
    State           VARCHAR(20),
    Type            ENUM ("Work", "Home"),
    City_ID int NOT NULL,
    CONSTRAINT Adres_ID_FMT CHECK (Adres_ID REGEXP "^[0-9]{6}$"),
    CONSTRAINT Pincode_FMT CHECK (Pincode REGEXP "^[0-9]{6}$"),
    CONSTRAINT Adres_FK FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE CASCADE,
    CONSTRAINT Adres_PK PRIMARY KEY (Customer_ID, Adres_ID),
	CONSTRAINT adres_ibfk_1 FOREIGN KEY (City_ID) REFERENCES City (City_ID)
);

CREATE TABLE Orders (
    Order_ID            CHAR(10),
    Customer_ID         CHAR(6),
    Adres_ID          CHAR(6),
    Total_Price         NUMERIC(6, 0) UNSIGNED DEFAULT 0,
    Payment_Method      ENUM ("Cash On Delivery", "Debit Card", "Credit Card", "Net Banking"),
    Status              ENUM ("Delivered", "Not Delivered"),
    Order_Date          TIMESTAMP, 
    CONSTRAINT Orders_ID_FMT CHECK (Order_ID REGEXP "^[A-Z]{2}-[0-9]{7}$"),
    CONSTRAINT Orders_Total_Price CHECK (Total_Price >= 0),
    CONSTRAINT Orders_PK PRIMARY KEY (Order_ID),
    CONSTRAINT Orders_FK FOREIGN KEY (Customer_ID, Adres_ID) REFERENCES Adres (Customer_ID, Adres_ID) ON DELETE CASCADE
);


CREATE TABLE Delivery (
    Order_ID        CHAR(10), 
    ID              CHAR(6),
    CONSTRAINT Delivery_FK_1 FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID) ON DELETE CASCADE,
    CONSTRAINT Delivery_PK PRIMARY KEY (Order_ID, ID)
);

CREATE TABLE Product (
    Product_ID      CHAR(10),
    Name            VARCHAR(20),
    Category        VARCHAR(20),
    Price           NUMERIC(6, 0) UNSIGNED DEFAULT 0,
    Rating          NUMERIC(2, 1) UNSIGNED DEFAULT 0,
    Seller          VARCHAR(20),
    Quantity        NUMERIC(3, 0) UNSIGNED DEFAULT 0,
    CONSTRAINT Product_ID_FMT CHECK (Product_ID REGEXP "^[A-Z]{3}-[0-9]{6}$"),
    CONSTRAINT Product_Price CHECK (Price >= 0),
    CONSTRAINT Product_Rating CHECK (Rating >= 0 and Rating <= 5),
    CONSTRAINT Product_PK PRIMARY KEY (Product_ID)
);

CREATE TABLE Cart (
    Customer_ID     CHAR(6),
    Prod_ID1        CHAR(10),
    Prod_ID2        CHAR(10),
    Prod_ID3        CHAR(10),
    Prod_ID4        CHAR(10),
    Prod_ID5        CHAR(10),
    CONSTRAINT Cart_Customer_ID_FK FOREIGN KEY (Customer_ID) REFERENCES Customer (Customer_ID) ON DELETE CASCADE,
    CONSTRAINT Cart_Prod_ID1_FK FOREIGN KEY (Prod_ID1) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID2_FK FOREIGN KEY (Prod_ID2) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID3_FK FOREIGN KEY (Prod_ID3) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID4_FK FOREIGN KEY (Prod_ID4) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Cart_Prod_ID5_FK FOREIGN KEY (Prod_ID5) REFERENCES Product (Product_ID) ON DELETE SET NULL,
    CONSTRAINT Customer_PK PRIMARY KEY (Customer_ID)
);

CREATE TABLE OrderDetails (
    Order_ID        CHAR(10),
    Product_ID      CHAR(10),
    CONSTRAINT OrderDetails_FK_1 FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID) ON DELETE CASCADE,
    CONSTRAINT OrderDetails_FK_2 FOREIGN KEY (Product_ID) REFERENCES Product (Product_ID) ON DELETE CASCADE
);

CREATE TABLE Rating (
 Rating_ID int NOT NULL AUTO_INCREMENT,
 Order_ID int NOT NULL,
 Rate int NOT NULL,
 Comment varchar(30) DEFAULT NULL,
 PRIMARY KEY (Rating_ID)
);