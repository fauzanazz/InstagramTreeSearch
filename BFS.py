import cv2
import instaloader
import numpy as np

import StringCompare
import ImageCompare
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


class BFS:
    """Breadth First Search Algorithm Integrated with Instagram Profile Comparator"""

    def __init__(self, queue: list[instaloader.Profile], visited: set, target_username: str = None,
                 target_photo: cv2.typing.MatLike = None, using_name: bool = False, using_photo: bool = False):
        self.queue = queue
        self.visited = visited
        self.target_username = target_username
        self.target_photo = target_photo
        self.found = False
        self.result: list[instaloader.Profile] = []
        self.using_name = using_name
        self.using_photo = using_photo

    async def fetch_photo(self, url):
        """Fetch profile photo asynchronously."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def compare_photos_async(self, profiles):
        """Fetch and compare profile photos asynchronously."""
        tasks = []
        for profile in profiles:
            if profile.is_private:
                continue
            tasks.append(self.fetch_photo(profile.profile_pic_url))

        photos = await asyncio.gather(*tasks)
        results = []
        for photo in photos:
            image = cv2.imdecode(np.frombuffer(photo, np.uint8), cv2.IMREAD_COLOR)
            results.append(ImageCompare.ImageCompare(image, self.target_photo).is_face_match())
        return results

    def compare_names(self, profiles):
        """Compare profile names using multiprocessing."""
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            results = list(executor.map(
                lambda profile: StringCompare.StringCompare(profile.full_name, self.target_username).substring(),
                profiles
            ))
        return results

    async def bfs(self):
        """Breadth First Search Algorithm"""
        batch_size = 10  # Number of profiles to process in parallel
        queue = self.queue.copy()
        while queue:  # while queue is not empty
            batch = [queue.pop(0) for _ in range(min(batch_size, len(queue)))]
            self.visited.update(batch)

            name_results = []
            photo_results = []

            if self.using_name:
                name_results = self.compare_names(batch)

            if self.using_photo:
                photo_results = await self.compare_photos_async(batch)

            for i, profile in enumerate(batch):
                if (self.using_name and name_results[i]) or (self.using_photo and photo_results[i]):
                    self.found = True
                    self.result.append(profile)

        return self.found

    def get_queue(self) -> list[instaloader.Profile]:
        return self.queue

    def get_found(self) -> bool:
        return self.found

    def get_result(self) -> list[instaloader.Profile]:
        return self.result
