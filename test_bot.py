from poetry_bot import PoetryBot

def main():
    bot = PoetryBot()
    try:
        bot.monitor_chat()
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main() 