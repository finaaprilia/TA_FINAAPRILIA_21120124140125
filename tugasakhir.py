import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

class Member:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.points = 0
        self.history = []  
        self.vouchers = []

    def add_points(self, amount):
        if amount == 25000:
            self.points += 20
        elif amount == 30000:
            self.points += 25
        elif amount == 35000:
            self.points += 30
        elif amount == 40000:
            self.points += 35
        if self.points >= 100:
            self.points -= 100
            self.vouchers.append("Free 1 cup coffee")

    def get_points(self):
        return self.points

    def get_vouchers(self):
        return self.vouchers

    def add_history(self, item, price):
        self.history.append((item, price))

    def get_all_history(self):
        return list(reversed(self.history))

class KopikuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kopiku")
        self.root.geometry("400x500")
        self.root.configure(bg="#f5f5dc") 
        self.members = {}
        self.current_user = None

        self.members["lily"] = Member("lily", "12345")
       
        try:
            self.icon = PhotoImage(file="coffee.png")
            self.icon = self.resize_icon(self.icon, 110, 110)
        except Exception:
            self.icon = None

        self.font_primary = ("Arial Black", 14, "bold")
        self.font_secondary = ("Arial Black", 12)
        self.login_frame()

    def resize_icon(self, icon, width, height):
        return icon.subsample(int(icon.width() // width), int(icon.height() // height))

    def create_oval_button(self, canvas, x, y, width, height, text, bg, fg, command):
        oval = canvas.create_oval(
            x - width // 2, y - height // 2, x + width // 2, y + height // 2, fill=bg, outline=""
        )
        label = canvas.create_text(x, y, text=text, font=("Arial Black", 12), fill=fg)

        canvas.tag_bind(oval, "<Button-1>", lambda event: command())
        canvas.tag_bind(label, "<Button-1>", lambda event: command())

    def login_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to Kopiku! ☕", font=("Arial Black", 20, "bold"), bg="#f5f5dc").pack(pady=20)
        if self.icon:
            canvas = tk.Canvas(self.root, width=100, height=100, bg="#f5f5dc", highlightthickness=0)
            canvas.create_image(50, 50, image=self.icon)
            canvas.pack()
        tk.Label(self.root, text="Please login to continue 🚀", font=("Arial black", 10), bg="#f5f5dc").pack(pady=10)
        tk.Label(self.root, text="Username 👤", font=self.font_secondary, bg="#f5f5dc").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=self.font_secondary, bd=2, relief="groove")
        self.username_entry.pack()
        tk.Label(self.root, text="Password 🔑", font=self.font_secondary, bg="#f5f5dc").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=self.font_secondary, bd=2, relief="groove", show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Login", font=self.font_secondary, bg="#D2B48C", fg="black", command=self.login).pack(pady=10)

    def menu_frame(self):
        self.clear_frame()

        tk.Label(
            self.root, text=f"Welcome, {self.current_user.username}!", font=("Arial Black", 18, "bold"), bg="#f5f5dc"
        ).pack(pady=20)

        canvas = tk.Canvas(self.root, width=400, height=360, bg="#f5f5dc", highlightthickness=0)
        canvas.pack()

        self.create_oval_button(canvas, 200, 50, 200, 50, "Order Coffee", "#D2B48C", "black", self.order_frame)
        self.create_oval_button(canvas, 200, 120, 200, 50, "Check Points", "#D2B48C", "black", self.check_points)
        self.create_oval_button(canvas, 200, 190, 200, 50, "Vouchers", "#D2B48C", "black", self.view_vouchers)
        self.create_oval_button(canvas, 200, 260, 200, 50, "History", "#D2B48C", "black", self.view_history)
        self.create_oval_button(canvas, 200, 330, 150, 50, "Logout", "#8B4513", "white", self.logout)

    def order_frame(self):
        self.clear_frame()

        tk.Label(self.root, text="Pilih Menu", font=("Arial Black", 18, "bold"), bg="#f5f5dc").pack(pady=20)
        self.menu = [
            ("Americano", 25000),
            ("Latte", 30000),
            ("Cappuccino", 35000),
            ("Machiato", 40000),]

        for item, price in self.menu:
            tk.Button(
                self.root,
                text=f"{item} - Rp {price}",
                font=self.font_secondary,
                bg="#D2B48C",
                fg="black",
                command=lambda i=item, p=price: self.order_item(i, p),
            ).pack(pady=5)
        tk.Button(
            self.root,
            text="Back to Menu",
            font=self.font_secondary,
            bg="#f4b183",
            fg="black", 
            command=self.menu_frame,
        ).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.members and self.members[username].password == password:
            self.current_user = self.members[username]
            self.menu_frame()
        else:
            messagebox.showerror("Error", "Invalid Username or Password!")

    def order_item(self, item, price):
        self.current_user.add_points(price)
        self.current_user.add_history(item, price)
        points = self.current_user.get_points()
        messagebox.showinfo("Order", f"Pesanan {item} berhasil. Kamu mendapat {points} poin.")

    def check_points(self):
        points = self.current_user.get_points()
        messagebox.showinfo("Check Points", f"Kamu punya {points} poin nih. Kumpulkan 100 poin untuk nikmati vouchermu!")

    def view_vouchers(self):
        vouchers = self.current_user.get_vouchers()
        if vouchers:
            messagebox.showinfo("Vouchers", "\n".join(vouchers))
        else:
            messagebox.showinfo("Vouchers", "Yah, belum ada voucher yang bisa dipakai.")

    def view_history(self):
        history = self.current_user.get_all_history()
        if history:
            history_text = "\n".join([f"{item} - Rp {price}" for item, price in history])
            messagebox.showinfo("History", history_text)
        else:
            messagebox.showinfo("History", "Belum ada transaksi.")

    def logout(self):
        self.current_user = None
        self.login_frame()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KopikuApp(root)
    root.mainloop()
