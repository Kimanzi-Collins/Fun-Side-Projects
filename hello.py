import socket
import sys

def play_star_wars():
    # The legendary server hosting the ASCII Star Wars
    host = 'towel.blinkenlights.nl'
    port = 23

    print("Establishing connection to a galaxy far, far away...")

    try:
        # Open a raw TCP connection to the Telnet port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            
            while True:
                # Receive the data chunks from the server
                chunk = s.recv(1024)
                if not chunk:
                    break
                
                # Print directly to stdout for the animation effect
                sys.stdout.write(chunk.decode('utf-8', errors='ignore'))
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\nTransmission terminated. May the Force be with you!")
    except Exception as e:
        print(f"\nError: The Empire jammed our signal ({e})")
        print("Alternatively, try running: ssh starwarstel.net directly in your terminal!")

if __name__ == '__main__':
    play_star_wars()