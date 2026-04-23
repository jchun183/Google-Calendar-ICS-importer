# 📅 Google Calendar ICS Importer

## 📦 Setup Instructions (One-Time)

### 1. Extract the Folder

Download and extract the folder anywhere on your computer
(e.g. Desktop, Documents, Downloads — anywhere works)

---

### 2. Install Right-Click Option

Double-click:

```
setup.bat
```

This will add:

> **"Import to Google Calendar"** to your right-click menu for `.ics` files

---

### 3. You're Done ✅

---

## 📌 How to Use

1. Right-click any `.ics` file
2. Click:

   ```
   Import to Google Calendar
   ```
3. Done 🎉

---

## 🔐 First Time Only (Google Login)

The first time you run it:

* A browser will open
* Sign into your Google account
* Click **Allow**

After that:

* You won’t need to log in again
* It works instantly

---

## ⚠️ Notes

* If you don’t see the option right away:

  * Right-click → **Show more options** (Windows 11)
  * Or restart File Explorer

* You must have **Python installed** on your computer
  👉 https://www.python.org/downloads/

---

## 🧠 What’s Included

```
import_ics.py              → Main script
import_to_calendar.bat     → Runs the script
setup.bat                  → Installs right-click option
credentials.json           → Google API credentials
```

---

## ❗ Important

Do **NOT** share or reuse `token.json`
It is created automatically when you log in and is tied to your account.

---

## 🧼 Troubleshooting

### “Python not found”

Install Python and try again.

---

### “Access blocked / Google verification”

Make sure your email has been added as a **test user** in Google Cloud Console.

---

### Nothing happens when clicking

* Make sure Python is installed
* Try double-clicking `import_to_calendar.bat` directly to test

---

## 💡 Optional Improvements

* Works great with downloaded meeting invites
* Can be extended to auto-import from Gmail (advanced)

---

## 🎉 Enjoy!

No more manual importing — just right-click and go 🚀
