import aiohttp
import os
import zipfile as zf
import shutil
import asyncio

from gofilepy import GofileClient
from gofilepy.exceptions import GofileAPIException

media_ext = (".png",".jpg",".gif",".mp4",".webm","mov")



async def download_file(url:str, folder_path:str,file_name:str) -> tuple[str, bool, str|None]:
    failed = False
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                failed = True
                return url, failed, None
            else:
                data = await response.read()
                path = os.path.join(folder_path, file_name)
                with open(path, "wb") as f:
                    f.write(data)
                return url, failed, path


def zip_files(folder_path:str, zip_save_location:str, zip_name:str):
    os.makedirs(zip_save_location, exist_ok=True)


    zip_name = os.path.join(zip_save_location, f"{zip_name}.zip")
    with zf.ZipFile(zip_name, "w") as zipf:
        for file in os.listdir(folder_path):
            zipf.write(os.path.join(folder_path, file), arcname=file)

    return zip_name


async def send_file(file_path:str):
    status = True
    gofile: GofileClient = await connect_to_gofile()
    if gofile is None:
        status = False
        return "Failed to connect to Gofile", status
    gofile_resp = gofile.upload(file=open(file_path, "rb"))
    link = gofile_resp.page_link
    return link, status


async def connect_to_gofile():
    retry_count = 0
    while retry_count < 5:
        try:
            return GofileClient()
        except GofileAPIException:
            await asyncio.sleep(1)
            retry_count += 1
    print("Failed to connect to Gofile")
    return None




def clean_up(folder_path: str):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

