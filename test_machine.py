from zk import ZK
import traceback

# ==========================
# Device Configuration
# ==========================
IP = "192.168.0.130"
PORT = 4370
PASSWORD = 123456,
TIMEOUT = 20

# ==========================
# Connect
# ==========================
zk = ZK( 
    IP,
    port=4370,
    timeout=30,
    password= 123456,
    force_udp=True,
    ommit_ping=True,
    verbose=True
)

try:
    print("=" * 50)
    print("Connecting to Attendance Machine...")
    print("=" * 50)

    conn = zk.connect()

    print("✅ Connected Successfully")

    # Disable device while downloading
    conn.disable_device()

    # --------------------------
    # Users
    # --------------------------
    users = conn.get_users()

    print(f"\nTotal Users : {len(users)}")

    for user in users:
        print(
            f"ID={user.user_id} | "
            f"Name={user.name} | "
            f"UID={user.uid}"
        )

    # --------------------------
    # Attendance Logs
    # --------------------------
    attendance = conn.get_attendance()

    print(f"\nTotal Attendance Records : {len(attendance)}")

    print("\nFirst 20 Records:\n")

    for log in attendance[:20]:
        print(log)

    # Enable device again
    conn.enable_device()

    conn.disconnect()

    print("\n✅ Download Completed Successfully")

except Exception as e:

    print("\n❌ Connection Failed")
    print("Error :", e)

    traceback.print_exc()