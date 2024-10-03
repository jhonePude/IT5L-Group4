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
        
        textfield3.delete(0, tk.END)
        textfield3.insert(0, values[2])
        
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
                
                messagebox.showerror("Input Error", "Product Quantity or Product Price must be a valid number \n Please Fill All Fields!")
                myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                
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
           
            confirmm = messagebox.askyesno("Confirmation", "Do you want to continue?") 
            if confirmm:  
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
                
            combobox =combo.get()
            
            cursor = connection.cursor()
            cursor.execute("SELECT Product_Name FROM stocks WHERE Product_ID = %s", (prdct_id,))
            db_prduct_id = cursor.fetchone()
            
            d = datetime.datetime.now()
            prdct_addate = d.strftime('%m/%d/%Y')

            
            
            if db_prduct_id:     
                messagebox.showerror("Error", f"{prdct_id} Already Existed in Database! ")
            else:
                
                        
                if  prdct_id and prdct_name and prdct_price and prdct_qty and prdct_addate and prdct_expire and combobox:
                            
                        
                        for itemss in tree.get_children():
                            
                            row_daata.append(tree.item(itemss, "values")[0])
                            row_daata.append(tree.item(itemss, "values")[1])
                            
                        if prdct_id in row_daata:
                        
                            messagebox.showerror("Error", f"{prdct_id} Already Existed! ")
                            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield7)
                            combo.set("-Empty-") 
                        
                        elif combobox == "-Empty-":
                        
                            messagebox.showerror("Error" , "User Name is Empty")
                            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield7)
                            combo.set("-Empty-")
                        
                        else:
                            
                            try:
                                
                                datetime.datetime.strptime(prdct_expire, '%m/%d/%Y')
                                
                            except ValueError:
                                
                                messagebox.showerror("Error", "Invalid date format! Please enter the date in MM/DD/YYYY format \n  EXAMPLE: 01/11/2011.")
                                myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                                combo.set("-Empty-")
                                
                            else:
                                # add image path and product_id in the .txt
                                if file_path: 
                                    with open(file_path, 'rb') as file:
                                        image_data = file.read()
                                        
                                image_file_path = os.path.abspath(file_path)
                                
                                with open('stocksimages.txt', 'a') as imagesfile:
                                    imagesfile.write(f"{prdct_id},{image_file_path},{combobox}\n")
                                    
                                # add data in treeview
                                prduct_id = prdct_id.capitalize()
                                # int_prdct_id = int(prdct_id)
                                tree.insert("", tk.END, values=(prduct_id, prdct_name, float(prdct_price), int(prdct_qty) , prdct_addate, prdct_expire, combobox ))
                                
                                #add data in database stocks
                                cursor = connection.cursor()
                                cursor.execute("INSERT INTO Stocks (Product_ID, Product_Name, Product_Price, Product_Quantity, Product_Added_Date, Product_Expiration, Product_Image, userName, userID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(prduct_id, prdct_name, prdct_price,  prdct_qty , prdct_addate, prdct_expire, image_file_path, combobox, userID))
                                connection.commit()
                                
                                # auto clear textfields
                                myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)

                                messagebox.showinfo("Save ","Saved Successfully!" )  
                                combo.set("-Empty-") 
                else:
                        messagebox.showerror("Error", f"Please fill all fields!")   
                    
        
############################################################################################

               
     def updated_row_on_click(textfield1,textfield2,textfield3,textfield5,textfield7,selected_row, connection,tree):
           
                if selected_row:
                   
                    # Keep the existing Product_ID
                    # id = tree.item(selected_row)['values'][0]  
                    # name = textfield2.get()
                    # price = textfield3.get()
                    # userName =tree.item(selected_row)['values'][3]  
                    
                    d = datetime.datetime.now()

                    updateddate = d.strftime('%m/%d/%Y  %H:%M %p')
                    addeddate = d.strftime('%m/%d/%Y')
                    
                    id = tree.item(selected_row)['values'][0]   
                    name = textfield2.get()
                    price = float(textfield3.get())
                    quantity = textfield5.get()
                    expiration = textfield7.get()
                    userName =tree.item(selected_row)['values'][6]  
                    
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
                             cursor1.execute("UPDATE Stocks SET Product_Name = %s, Product_Price = %s,  Product_Quantity = %s, Product_Added_Date = %s, Product_Expiration = %s, userName = %s WHERE Product_ID = %s", (name, price, quantity, addeddate, expiration ,userName, id))
                             connection.commit()    
                            
                             cursor2 = connection.cursor()
                             query = " INSERT INTO `UPDATED STOCKS` (product_id, product_name, product_price, product_quantity, product_expiration, userName, updated_date, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                             cursor2.execute(query, (id, name, price, quantity, expiration, userName, updateddate, userID))
                             connection.commit()

                             # Update the selected row in the Treeview
                             tree.item(selected_row, values=(id, name, price, quantity, addeddate, expiration, userName))
                        
                             myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5,textfield7)
                             messagebox.showinfo("Updated ","Updated Successfully! \n ⚠️ Product ID is Not Updatable! ")

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
            deleteddate = d.strftime('%m/%d/%Y  %H:%M %p')

            
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
             

            myclass.auto_delete_texfields(textfield1,textfield2,textfield3,textfield5, textfield7)
            
            

            messagebox.showinfo("Delete ","Deleted Successfully!")
            

        return 
     
############################################################################################

   
     def searchbox(product_id,tree,connection,label5,textfield1,textfield2,textfield3,textfield5,textfield7,combo):
            if  product_id:
                if  product_id != "":
                            
                        with open('stocksimages.txt', 'r') as imagesfile:
                            for line in imagesfile:
                                saved_image_path = line.strip().split(',')  # Assuming each line is formatted like "prdct_id,filepath"
                                if saved_image_path[0] == str(product_id) and saved_image_path[2] == str(combo.get()) :  # Compare product ID
                                    image_file_path = saved_image_path[1]  # Get the corresponding image file path
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
                

            
        
                
