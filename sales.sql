CREATE TABLE Employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100),
    Address VARCHAR(255),
    Email VARCHAR(100),
    Role VARCHAR(50)
);

CREATE TABLE Store (
    StoreID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100)
);
-- Product Table
CREATE TABLE Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100),
    Price DECIMAL(10, 2),
    StoreID INT,
    FOREIGN KEY (StoreID) REFERENCES Store(StoreID)
);

-- Customer Table
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(100),
    Address VARCHAR(255),
    Email VARCHAR(100)
);

-- Order Table
CREATE TABLE Orders (
    OrderNumber INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderDate DATE,
    CustomerID INT,
    ProductID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
-- Insert Employees
INSERT INTO Employee (EmployeeID, Name, Address, Email,Role) VALUES
(1, 'Rajesh Kumar', 'Mumbai, Maharashtra', 'rajesh.kumar@email.com','Admin'),
(2, 'Anjali Sharma', 'Delhi, India', 'anjali.sharma@email.com', 'SalesManager'),
(3, 'Vikram Patel', 'Ahmedabad, Gujarat', 'vikram.patel@email.com', 'SalesManager'),
(4, 'Priya Desai', 'Chennai, Tamil Nadu', 'priya.desai@email.com', 'ProductManager'),
(5, 'Suresh Gupta', 'Bangalore, Karnataka', 'suresh.gupta@email.com', 'ProductManager');

INSERT INTO Store (StoreID, Name) VALUES
(1, 'Reliance Digital'),
(2, 'Big Bazaar'),
(3, 'Croma'),
(4, 'Amazon India'),
(5, 'Flipkart');

-- Insert Product
INSERT INTO Product (ProductID, Name, Price, StoreID) VALUES
(1, 'Samsung Galaxy S21', 74999.99, 1),
(2, 'Mi 11', 35999.99, 2),
(3, 'Sony Bravia 55 inch', 84999.99, 3),
(4, 'Apple iPhone 12', 79999.99, 1),
(5, 'HP Pavilion Laptop', 62999.99, 4),
(6, 'OnePlus 9 Pro', 64999.99, 2),
(7, 'LG Washing Machine', 29999.99, 5),
(8, 'Nokia 8.3', 42999.99, 3),
(9, 'Dell XPS 13', 109999.99, 4),
(10, 'Canon EOS Camera', 59999.99, 1),
(11, 'Philips Air Fryer', 8999.99, 5),
(12, 'JBL Bluetooth Speaker', 4999.99, 2),
(13, 'Realme Smart TV', 24999.99, 1),
(14, 'Bose Noise Cancelling Headphones', 29999.99, 3),
(15, 'Asus ROG Laptop', 89999.99, 4),
(16, 'Samsung 32 inch TV', 22999.99, 1),
(17, 'Lenovo ThinkPad', 74999.99, 5),
(18, 'Wacom Intuos Pro', 25999.99, 2),
(19, 'Xiaomi Mi Band 6', 3499.99, 3),
(20, 'Beats Studio 3', 24999.99, 4),
(21, 'Motorola Edge Plus', 74999.99, 5),
(22, 'Bajaj 1.5 Ton AC', 38999.99, 1),
(23, 'Apple iPad Air', 54999.99, 4),
(24, 'Boat Rockerz Headphones', 3999.99, 2),
(25, 'Panasonic 43 inch TV', 34999.99, 3);

-- Insert Customer
INSERT INTO Customer (CustomerID, Name, Address, Email) VALUES
(1, 'Ravi Verma', 'Mumbai, Maharashtra', 'ravi.verma@email.com'),
(2, 'Sita Yadav', 'Delhi, India', 'sita.yadav@email.com'),
(3, 'Amit Mishra', 'Kolkata, West Bengal', 'amit.mishra@email.com'),
(4, 'Neha Mehta', 'Bangalore, Karnataka', 'neha.mehta@email.com'),
(5, 'Arvind Singh', 'Jaipur, Rajasthan', 'arvind.singh@email.com'),
(6, 'Deepika Patel', 'Vadodara, Gujarat', 'deepika.patel@email.com'),
(7, 'Sandeep Reddy', 'Hyderabad, Telangana', 'sandeep.reddy@email.com'),
(8, 'Manish Kumar', 'Chennai, Tamil Nadu', 'manish.kumar@email.com'),
(9, 'Priyanka Sharma', 'Lucknow, Uttar Pradesh', 'priyanka.sharma@email.com'),
(10, 'Rohit Sharma', 'Indore, Madhya Pradesh', 'rohit.sharma@email.com'),
(11, 'Anita Rao', 'Surat, Gujarat', 'anita.rao@email.com'),
(12, 'Mohammad Ali', 'Agra, Uttar Pradesh', 'mohammad.ali@email.com'),
(13, 'Tanya Gupta', 'Bhubaneswar, Odisha', 'tanya.gupta@email.com'),
(14, 'Kiran Patel', 'Pune, Maharashtra', 'kiran.patel@email.com'),
(15, 'Vishal Verma', 'Mumbai, Maharashtra', 'vishal.verma@email.com'),
(16, 'Sumit Arora', 'Delhi, India', 'sumit.arora@email.com'),
(17, 'Seema Gupta', 'Chandigarh, India', 'seema.gupta@email.com'),
(18, 'Krishna Yadav', 'Delhi, India', 'krishna.yadav@email.com'),
(19, 'Aishwarya Singh', 'Bhopal, Madhya Pradesh', 'aishwarya.singh@email.com'),
(20, 'Vikash Kumar', 'Patna, Bihar', 'vikash.kumar@email.com'),
(21, 'Rajeev Soni', 'Kanpur, Uttar Pradesh', 'rajeeve.soni@email.com'),
(22, 'Sonal Patel', 'Ahmedabad, Gujarat', 'sonal.patel@email.com'),
(23, 'Kavita Mehra', 'Mumbai, Maharashtra', 'kavita.mehra@email.com'),
(24, 'Sanjay Sharma', 'Bangalore, Karnataka', 'sanjay.sharma@email.com'),
(25, 'Geeta Kumari', 'Bhubaneswar, Odisha', 'geeta.kumari@email.com');

-- Insert Orders
INSERT INTO Orders (OrderNumber, OrderDate, CustomerID, ProductID) VALUES
(1, '2025-04-10', 1, 1),
(2, '2025-04-10', 2, 2),
(3, '2025-04-11', 3, 3),
(4, '2025-04-12', 4, 4),
(5, '2025-04-13', 5, 5),
(6, '2025-04-14', 6, 6),
(7, '2025-04-15', 7, 7),
(8, '2025-04-16', 8, 8),
(9, '2025-04-17', 9, 9),
(10, '2025-04-18', 10, 10),
(11, '2025-04-18', 11, 11),
(12, '2025-04-19', 12, 12),
(13, '2025-04-19', 13, 13),
(14, '2025-04-20', 14, 14),
(15, '2025-04-21', 15, 15),
(16, '2025-04-21', 16, 16),
(17, '2025-04-22', 17, 17),
(18, '2025-04-23', 18, 18),
(19, '2025-04-23', 19, 19),
(20, '2025-04-24', 20, 20),
(21, '2025-04-24', 21, 21),
(22, '2025-04-25', 22, 22),
(23, '2025-04-25', 23, 23),
(24, '2025-04-26', 24, 24),
(25, '2025-04-26', 25, 25);