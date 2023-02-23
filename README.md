# InstaFood's Website

InstaFood's Website is a simple Flask-Sqlite3 food ordering website. This website allows users to order food items online and have them delivered to their location.

## Requirements:

To use the InstaFood Website, you must have Python version 3.6 or later installed on your machine.

## How to install

To install the InstaFood's Website and run it locally, follow these steps:

1. Clone the repository:

```sh
git clone https://github.com/instafood-tunisia/website
```

2. Install dependencies:

```sh
pip install flask flask-wtf waitress
```

3. Start the web-server:

```sh
PASSWORD="admin_password" python3 .
```

Substitute the `admin_password` with the preferred password for the admin account.

## Usage:

Once you setup everything, you can access it through your web browser by navigating to http://localhost:6969.

From there, you can browse the available food items, select the items you want to order, and place your order. You can also view your order history, track the status of your current order, and update your account information.

In addition to placing orders and managing account information, you can also view all orders and manage menu items by accessing the admin panel at http://localhost:6969/admin. From the admin panel, you can view and manage all orders placed on the website, as well as add, remove, or update menu items. Note that you will need to log in as an admin with the correct credentials to access the admin panel.

## Authors and License:

The InstaFood Website was developed by [@akatiggerx04](https://github.com/akatiggerx04) with contributions from @salimslamadev. The code is licensed under the AGPL license, which permits anyone to use, modify, and distribute the code, including the original author. However, any modifications made to the code must also be licensed under AGPL, and the source code must be made available to anyone who uses the software. Please note that the images used in the website are owned by InstaFood and are not included in the AGPL license.