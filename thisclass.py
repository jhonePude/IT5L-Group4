from tkinter import messagebox 
import tkinter as tk 
from tkinter import ttk, Tk, filedialog
from PIL import Image, ImageTk
import io
import sv_ttk
import pywinstyles, sys 
import darkdetect
import runpy
import hashlib
import bcrypt
import os
import datetime
import customtkinter
from tkinter import scrolledtext


class myclass:  
    
 
 
     def auto_delete_texfields(textfield1, textfield2, textfield3, textfield5,textfield7):
        textfield1.delete(0, tk.END)  
        textfield2.delete(0, tk.END)  
        textfield3.delete(0, tk.END) 
        textfield5.delete(0, tk.END)   
        textfield7.delete(0, tk.END) 
        
        
     def row_clicked_auto_delete_texfields(values, textfield1, textfield2, textfield3, textfield5, textfield7):

        textfield1.delete(0, tk.END)
        textfield1.insert(0, values[0])
        
        textfield2.delete(0, tk.END)
        textfield2.insert(0, values[1])
        
        prductprice = values[2]
        price_as_float = float(prductprice.replace('₱', '').replace(',', ''))
        price_as_int = int(price_as_float)
        
        textfield3.delete(0, tk.END)
        textfield3.insert(0, price_as_int)
        
        textfield5.delete(0, tk.END)
        textfield5.insert(0, values[3])
        
        textfield7.delete(0, tk.END)
        textfield7.insert(0, values[5])
        
     def selected_row_on_click(textfield1, textfield2, textfield3, textfield5, textfield7, selected_row, tree, connection):  
         if selected_row:
                item = tree.item(selected_row)
                values = item['values']
                prduct_id = item['values'][0]
               
                
                cursor = connection.cursor()
                cursor.execute("SELECT Product_Image FROM stocks WHERE Product_ID = %s", (prduct_id,))
                result = cursor.fetchone()
                
                if result and result[0]:
                    image_data = result[0]
                    
                    image = Image.open(io.BytesIO(image_data))
                    image.thumbnail((200, 200))  
                    photo = ImageTk.PhotoImage(image)
                   
         myclass.row_clicked_auto_delete_texfields(values,textfield1,textfield2,textfield3, textfield5, textfield7)

############################################################################################
         
     def num_checker_get_values(textfield1,textfield2,textfield3,textfield5,textfield7):
            prdct_name = textfield2.get()
            prdct_id = textfield1.get()
            prdct_qty = textfield5.get()
            prdct_expire= textfield7.get()
            
            try:      
                prdct_price = float(textfield3.get())
                prdct_qty = int(textfield5.get())
             
            except ValueError:
                messagebox.showerror("Error", "Product ID and Product Price Must be numeric Value")
                return None, None, None  

            return prdct_id, prdct_name, float(prdct_price), int(prdct_qty), prdct_expire
        
############################################################################################
    
     def create_treeview(frame,style):
        
        sv_ttk.set_theme("light")
         
        columns = ('#1', '#2', '#3', '#4', '#5','#6','#7')
        column_names = ('Column 1', 'Column 2', 'Column 3','Column 4','Column 5','Column 6','Column 7')

        tree = ttk.Treeview(frame, columns=columns, show='headings')

        
        style.configure("Treeview.Heading", font=("Franklin Gothic Heavy", 14,"italic"))
        style.configure("Treeview", rowheight=80) 
        style.configure("Treeview", font=("Bahnschrift", 25,"bold"))
        style.map("Treeview", background=[('selected', '#87CEFA')]) 
    
        
    
        tree.heading('#1', text='Product ID')
        tree.column('#1', width=140, anchor="c")

        tree.heading('#2', text='Product Name')
        tree.column('#2', width=140, anchor="c")

        tree.heading('#3', text='Product Price')
        tree.column('#3', width=140, anchor="c")
        
        tree.heading('#4', text='Product Quantity')
        tree.column('#4', width=130, anchor="c")     
        
        tree.heading('#5', text='Date Added')
        tree.column('#5', width=130, anchor="c")      
        
        tree.heading('#6', text='Expiration')
        tree.column('#6', width=130, anchor="c") 
        
        tree.heading('#7', text='Username')
        tree.column('#7', width=130, anchor="c")  
       
       
        return tree
  
  
############################################################################################

 
     def add_row_on_click(prdct_id, prdct_name, prdct_price, prdct_qty, prdct_expire,tree, row_daata,userID,combo,connection,textfield1,textfield2,textfield3,textfield5,textfield7):
         
            textfield1.config(state="normal")
            confirmm = messagebox.askyesno("Confirmation", "Do you want to continue?") 
            
            if confirmm:  
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
                
            combobox =combo.get()
            
            cursor = connection.cursor()
            cursor.execute("SELECT Product_Name FROM stocks WHERE Product_ID = %s", (prdct_id,))
            db_prduct_id = cursor.fetchone()
            
            d = datetime.datetime.now()
            prdct_addate = d.strftime('%b/%d/%Y')
        
            prdct_price_rounded = (f"₱{float(prdct_price):.2f}")
            
            if db_prduct_id:     
                messagebox.showerror("Error", f"{prdct_id} Already Existed in Database! ")
            else:
                if prdct_id and prdct_name and prdct_price and prdct_qty and prdct_addate and prdct_expire and combobox:
                    for itemss in tree.get_children():
                        row_daata.append(tree.item(itemss, "values")[0])
                        row_daata.append(tree.item(itemss, "values")[1])
                        
                    if prdct_id in row_daata:
                        messagebox.showerror("Error", f"{prdct_id} Already Existed! ")
                        
                    elif combobox == "-Empty-":
                        messagebox.showerror("Error", "User Name is Empty")
                        
                    else:
                        # Change format date to this Ex: 08/22/2000 or Oct/22/2000
                        try:
                            prdct_expire = datetime.datetime.strptime(prdct_expire, '%m/%d/%Y')
                        except ValueError:
                            try:
                                prdct_expire = datetime.datetime.strptime(prdct_expire, '%b/%d/%Y')
                            except ValueError:
                                messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY or Month/DD/YYYY.\nEx: 08/22/2000 or Oct/22/2000")
                                return
                        prdct_expire_updated = prdct_expire.strftime('%b/%d/%Y')

                        # Add image path and product_id in the .txt file
                        if file_path: 
                            with open(file_path, 'rb') as file:
                                image_data = file.read()
                                
                            image_file_path = os.path.abspath(file_path)
                            
                            with open('stocksimages.txt', 'a') as imagesfile:
                                imagesfile.write(f"{prdct_id},{image_file_path},{combobox}\n")
                                
                        # Add data in Treeview
                        prduct_id = prdct_id.capitalize()
                        tree.insert("", tk.END, values=(prduct_id, prdct_name, prdct_price_rounded, int(prdct_qty), prdct_addate, prdct_expire_updated, combobox))
                        
                        myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)

                        # Add data in database stocks
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO Stocks (Product_ID, Product_Name, Product_Price, Product_Quantity, Product_Added_Date, Product_Expiration, Product_Image, userName, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (prduct_id, prdct_name, prdct_price_rounded, prdct_qty, prdct_addate, prdct_expire_updated, image_file_path, combobox, userID))
                        connection.commit()
                        
                        
                        messagebox.showinfo("Save", "Saved Successfully!")
                        combo.set("-Empty-")
                else:
                    messagebox.showerror("Error", "Please fill all fields!")

                    
        
############################################################################################

               
     def updated_row_on_click(textfield1,textfield2,textfield3,textfield5,textfield7,selected_row, connection,tree):
           
                if selected_row:
                    
                    d = datetime.datetime.now()

                    updateddate = d.strftime('%b/%d/%Y  %H:%M %p')
                    addeddate = d.strftime('%b/%d/%Y')
                    
                    id = tree.item(selected_row)['values'][0]   
                    name = textfield2.get()
                    price = float(textfield3.get())
                    quantity = textfield5.get()
                    
                    expiration = textfield7.get()
                    userName =tree.item(selected_row)['values'][6] 
                    
                    price_rounded = (f"₱{float(price):.2f}")
                   
                    
                     # Change format date to this Ex: 08/22/2000 or Oct/22/2000
                    try:
                        expiration_date = datetime.datetime.strptime(expiration, '%m/%d/%Y')
                    except ValueError:
                        try:
                            expiration_date = datetime.datetime.strptime(expiration, '%b/%d/%Y')
                        except ValueError:
                            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY or Month/DD/YYYY./nEx: 08/22/2000 or Oct/22/2000")
                            return
                    expiration_date_updated = expiration_date.strftime('%b/%d/%Y')
                    
                    cursor = connection.cursor()
                    cursor.execute("SELECT Product_ID FROM stocks WHERE Product_Name = %s", (id,))
                    db_prduct_id = cursor.fetchone()
                    
                    if db_prduct_id:
                        messagebox.showerror("Error", "Product ID is not Updatable! ")
                    else:
                    
                        if name and price:
                             
                            
                             with open('username.txt', 'r') as f:
                                current_username = f.read().strip()
        
                             cursor.execute("SELECT userID FROM account WHERE userName = %s", (current_username,))
                             userIDD = cursor.fetchone()
                            
                             if userIDD:  # Check if the user was found
                                userID = int(userIDD[0])
                                
                            
                             # Update the selected row  
                             cursor1 = connection.cursor()
                             cursor1.execute("UPDATE Stocks SET Product_Name = %s, Product_Price = %s,  Product_Quantity = %s, Product_Added_Date = %s, Product_Expiration = %s, userName = %s WHERE Product_ID = %s", (name, price_rounded, quantity, addeddate, expiration_date_updated ,userName, id))
                             connection.commit()    
                            
                             cursor2 = connection.cursor()
                             query = " INSERT INTO `UPDATED STOCKS` (product_id, product_name, product_price, product_quantity, product_expiration, userName, updated_date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                             cursor2.execute(query, (id, name, price_rounded, quantity, expiration_date_updated, userName, updateddate, userID))
                             connection.commit()

                             # Update the selected row in the Treeview
                             tree.item(selected_row, values=(id, name, price_rounded, quantity, addeddate, expiration_date_updated, userName))
                             
                             textfield1.config(state="normal")
                             myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                             messagebox.showinfo("Updated ","Updated Successfully! \n ⚠️ Product ID is Not Updatable! ")
                             textfield1.delete(0, tk.END) 

                        else:
                            messagebox.showerror("Error", f"please fill all fields! ")
                            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                        
                else:
                    messagebox.showerror("Error", f"Select A Row First! ") 
                    myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
        
    
############################################################################################

    
     def delete_selected_row(textfield1,textfield2,textfield3, textfield5, textfield7, selected_row, connection,tree):
        
        confirmm = messagebox.askyesno("Confirmation", "Do you want to continue to delete the selected row?") 
        
        if confirmm:               
            selected_item = tree.item(selected_row)
            values = selected_item["values"]
            product_id = values[0]  
            product_name = values[1]  
            product_price = values[2]  
            product_quantity= values[3] 
            product_addedate = values[4] 
            product_expiration = values[5] 
            
            cursor = connection.cursor()
            # Delete  row  sa database
            cursor.execute("DELETE FROM Stocks WHERE Product_ID = %s", (product_id,))
            connection.commit()

            d = datetime.datetime.now()
            deleteddate = d.strftime('%b/%d/%Y  %H:%M %p')

            
            # save in archive
            cursor.execute("INSERT INTO archive (product_id, product_name, product_price, product_quantity, product_added_date, product_expiration, deleted_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",(product_id, product_name, product_price, product_quantity, product_addedate, product_expiration, deleteddate))
            connection.commit()

            tree.delete(selected_row)  
            
       
            with open('stocksimages.txt', 'r') as imagesfile:
                lines = imagesfile.readlines()
            
            with open('stocksimages.txt', 'w') as imagesfile:
                
                for line in lines:
                    if not line.startswith(f"{product_id},"):  # Only write back lines that don't match the product ID
                        imagesfile.write(line)
             
            textfield1.config(state="normal")
            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5, textfield7)
            
            

            messagebox.showinfo("Delete ","Deleted Successfully!")
            

        return 
     
############################################################################################

   
     def searchbox(product_id,tree,connection,label5,textfield1,textfield2,textfield3,textfield5,textfield7,combo):
            if  product_id:
                if  product_id != "":
                            
                        with open('stocksimages.txt', 'r') as imagesfile:
                            for line in imagesfile:
                                saved_image_path = line.strip().split(',')  
                                if saved_image_path[0] == str(product_id) and saved_image_path[2] == str(combo.get()) :  # Compare product ID
                                    image_file_path = saved_image_path[1] 
                                    try:
                                        # Load and display the image
                                        image = Image.open(image_file_path)
                                        image = image.resize((200, 200))  
                                        photo = ImageTk.PhotoImage(image)
                                
                                        # Update the label with the new image
                                        label5.config(image=photo)
                                        label5.image = photo  
                                    except Exception as e:
                                        print(f"Error loading image: {e}")
                                
                                        
                                for row in tree.get_children():
                                    row_values = tree.item(row)['values']
                        
                                    if str(row_values[0]) == product_id:

                                        tree.selection_set(row)
                                        tree.see(row)  # Auto scroll to the row if it's not visible
                                        tree.item(row, tags=('highlight',))
                                        return
                                
                                messagebox.showerror("Error", "Product ID you entered does not exist.")
                                break
                                

                else:
                    messagebox.showerror("Error", "Product ID you entered is not Existed.")
                    label5.config(image=None)
                   
            else:
                messagebox.showerror("Error", " fill out the search box.")
#########################################################################################################3
# the code below is for log out in main menu
###################################################################################################
     def mainlogout(frame):
         confirmm = messagebox.askyesno("Logout", "Continue to Logout?") 
         if confirmm:
              
            frame.destroy()     
            os.system('python newlogin.py')
            
            with open("username.txt", 'w') as f:
                 f.write("")  
            return               
                
    
#########################################################################################################3
# the code below is for log in create accounts
###########################################################################################################
  
  
     def user_login_on_click(username,pasword,hushedpasword,connection,main_frame):
       
        query = "SELECT userID, userName, userPass FROM account WHERE userName = %s"

        cursor = connection.cursor()
        values = (username,)
        
        cursor.execute(query, values)  # Execute the query with parameters
        result = cursor.fetchone()
            
        if result:
                userID, db_username, db_hashed_password = result

                if hushedpasword.encode('utf-8') == (db_hashed_password.encode('utf-8')) and username == db_username:
                    
                    #pass username in textfile and access it in mainmenu 
                    with open('username.txt', 'w') as f:
                        f.write(username)
                        
                    query1 = "SELECT userName FROM account WHERE userID= %s"
                    val = (userID,)
                    cursor.execute(query1, val)
                    name = cursor.fetchone()
                    
                    messagebox.showinfo("Success", f"Welcome! {username}")
                     
                    main_frame.destroy()  
                    
                    os.system('python mainmenu.py')
                            
                else:
                    messagebox.showerror("Login Failed", "Invalid Password")
                
        else:
                messagebox.showerror("Login Failed", "Invalid Username")
                
     def validate_email(email):
        return email.endswith("@yahoo.com") or email.endswith("@gmail.com")
    
     def hompageinsignin(frame_userinputs):
        #2nd frame na mag show show username and password
            homepage = tk.Frame(frame_userinputs, bg= "light blue")
            homepage.pack(side=tk.LEFT)
            homepage.pack_propagate(False)
            homepage.pack()
            homepage.configure(width=650, height=600)
      
            return homepage
        
     def save_accountsforrememberme(textfield1_username,textfield2_password,check_button):
         
         if check_button.get():
             with open('accounts_rememberme.txt', 'w') as  f:
                f.write(f"{textfield1_username.get()} \n")
                f.write(f"{textfield2_password.get()} \n")
         else:
             with open('accounts_rememberme.txt', 'w') as  f:
                f.write(" ")
     
     def load_accountsforrememberme(textfield1_username,textfield2_password):
         try:
            with open('accounts_rememberme.txt', 'r') as myf:
                accounts = myf.readlines()
                if len(accounts) >= 2:
                    textfield1_username.insert(0,accounts[0].strip())
                    textfield2_password.insert(0,accounts[1].strip())
         except FileNotFoundError:
            pass
        
     def buttonarchived(connection):
         print("inside Deleted Stocks")
         newframe = Tk()
         newframe.geometry(f'{740}x{90}+{320}+{250}')
         newframe.title("DELETED STOCKS")
         newframe.resizable(False, False)
         
         cursor = connection.cursor()
         cursor.execute("SELECT * FROM archive")
         all_deleted_data = cursor.fetchall()
    
         text_area= scrolledtext.ScrolledText(newframe,wrap=tk.WORD, width=100, height =20)
         text_area.pack()
         
         for rows in all_deleted_data:
            text_area.insert(tk.INSERT,f'{rows}\n')
         text_area.config(state=tk.DISABLED)
         
            
     def button_updated_stocks(connection):
        print("inside updated stocks")
        
        newframe1 = Tk()
        newframe1.geometry(f'{740}x{90}+{320}+{250}')
        newframe1.title("Updated Stocks")
        newframe1.resizable(False, False)
         
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `UPDATED STOCKS`")
        updatedstocks = cursor.fetchall()
    
        text_area1= scrolledtext.ScrolledText(newframe1,wrap=tk.WORD, width=100, height =20)
        text_area1.pack()
         
        for rows in updatedstocks:
            text_area1.insert(tk.INSERT,f'{rows}\n')
        text_area1.config(state=tk.DISABLED)
    
     def on_radio_button_selected(radio_var):
        selected_value = radio_var.get()  
        if isinstance(selected_value, set):
             selected_value = next(iter(selected_value))  

        selected_value = selected_value.lower()
       
        return selected_value

        
    
    