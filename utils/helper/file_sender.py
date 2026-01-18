import aiohttp
import os
import zipfile as zf
import shutil

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
    upload_url = "https://upload.gofile.io/uploadfile"
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field(
            "file",
            open(file_path, "rb"),
            filename=os.path.basename(file_path)
        )

        async with session.post(upload_url, data=form) as resp:
            if resp.status != 200:
                return None, False
            result = await resp.json()
            if result.get("status") not in ("ok", "success"):
                return None, False

            return result["data"].get("downloadPage"), True





def clean_up(folder_path: str):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

