import Instagram
import BFS
import cv2
import time


def main():
    try:
        # Get user input
        username = input('Enter your Instagram username: ')
        password = input('Enter your Instagram password: ')

        while True:  # Loop until valid input is provided
            try:
                using_name = input('Do you want to use username comparison? (y/n): ')
                using_photo = input('Do you want to use photo comparison? (y/n): ')

                # Convert input to boolean
                if using_name.lower() == 'y':
                    using_name = True
                else:
                    using_name = False

                # Convert input to boolean
                if using_photo.lower() == 'y':
                    using_photo = True
                else:
                    using_photo = False

                break
            except Exception as e:
                print(f"Error: {e}")

        # Comparator Check
        if using_name:
            target_username = input('Enter the target username: ')
        else:
            target_username = None

        if using_photo:
            target_profile_path = input('Enter the target profile photo path: ')
            target_profile_img = cv2.imread(target_profile_path)
        else:
            target_profile_img = None

        if not using_name and not using_photo:
            print("Please select at least one comparison method")
            return

        # Login to Instagram
        insta = Instagram.Instagram(username, password)
        login_status, login_message = insta.login()

        if not login_status:  # If login failed
            print(login_message)
            return

        followers = insta.get_followers(username)
        if not followers:  # If no followers found
            print(f"No followers found for {username}")

        # Initialize BFS first depth
        visited = set()
        bfs = BFS.BFS(
            queue=followers,
            visited=visited,
            target_username=target_username,
            target_photo=target_profile_img,
            using_name=using_name,
            using_photo=using_photo
        )
        found = bfs.bfs()
        while not found:
            print("Target not found")
            # Continue BFS until target is found using the followers of last depth queue
            next_queue = []
            for last_queue in bfs.get_queue():
                next_followers = insta.get_followers(last_queue.username)
                if next_followers:
                    next_queue.extend(next_followers)
                    time.sleep(0.5)  # Sleep for 0.5 seconds to avoid rate limit

            bfs.queue = next_queue
            found = bfs.bfs()

        print("Target found")

        # Show the target profile details
        for profile in bfs.get_result():
            print(f"\nTarget Profile Details")
            print(f"Targer Link: https://www.instagram.com/{profile.username}")
            print(f"Username: {profile.username}")
            print(f"Full Name: {profile.full_name}")
            print(f"Profile Picture URL: {profile.profile_pic_url}")
            print(f"Biography: {profile.biography}")

        return

    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == '__main__':
    main()
