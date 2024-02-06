import json
import aiohttp
import shutil
import re
from pathlib import Path

from gen import gen_origin_mapping
from beta_update import gen_beta_mapping


EQUIPMENT_URL = "https://api.yatta.top/hsr/v2/cn/equipment/"
AVATAR_URL = "https://api.yatta.top/hsr/v2/cn/avatar/"
BETA_JSON_PATH = Path("beta_json")
RE_DATA = re.compile(r"<[^>]*>")


async def download(
    beta_avatar_list: list[int], beta_equipment_list: list[tuple[int, str]]
):
    async with aiohttp.ClientSession() as session:
        for beta_avatar_id in beta_avatar_list:
            async with session.get(AVATAR_URL + str(beta_avatar_id)) as response:
                data = await response.text()
                res = re.sub(RE_DATA, "", data)
                Path("beta_json/avatar").mkdir(parents=True, exist_ok=True)
                with open(
                    f"beta_json/avatar/{beta_avatar_id}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(json.dumps(json.loads(res), indent=4, ensure_ascii=False))
        for beta_equipment_tuple in beta_equipment_list:
            beta_equipment_id = beta_equipment_tuple[0]
            beta_equipment_main = beta_equipment_tuple[1].split(",")

            async with session.get(EQUIPMENT_URL + str(beta_equipment_id)) as response:
                data = await response.text()
                res = re.sub(RE_DATA, "", data)
                Path("beta_json/equipment").mkdir(parents=True, exist_ok=True)
                json_data = json.loads(res)
                if beta_equipment_main[0] == "":
                    json_data["data"]["skill"]["list"] = []
                else:
                    json_data["data"]["skill"]["list"] = beta_equipment_main

                with open(
                    f"beta_json/equipment/{beta_equipment_id}.json",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(json.dumps(json_data, indent=4, ensure_ascii=False))


async def main(enable_beta: bool):
    shutil.rmtree("output/gen")
    shutil.copytree("base_map", "output/gen")
    Path("beta_json/avatar").mkdir(parents=True, exist_ok=True)
    Path("beta_json/equipment").mkdir(parents=True, exist_ok=True)
    Path("output/excel").mkdir(parents=True, exist_ok=True)

    gen_origin_mapping()
    if enable_beta:
        print("Enable Beta Generate")
        beta_avatar_list: list[int] = [1305]
        beta_equipment: list[tuple[int, str]] = [
            (23019, ""),
            (23020, "CriticalDamageBase"),
            (23011, "HPAddedRatio,SPRatioBase"),
        ]

        await download(beta_avatar_list, beta_equipment)

        gen_beta_mapping(BETA_JSON_PATH)


if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="StraRailUID Map Generater")
    parser.add_argument("--beta", type=bool, default=False)

    args = parser.parse_args()
    enable_beta = args.beta

    asyncio.run(main(enable_beta))
