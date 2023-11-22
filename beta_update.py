import json
from pathlib import Path

from version import sr_version as version

Excel_path = Path(__file__).parent / "StarRailData" / "ExcelOutput"
StarRailRes_path = Path(__file__).parent / "StarRailRes"
beta_json_path = Path(__file__).parent / "beta_json"
gen_map_path = Path(__file__).parent / "output" / "gen"
pre_points_list = {
    "202": "101",
    "203": "202",
    "204": "203",
    "205": "102",
    "206": "205",
    "207": "206",
    "208": "103",
    "209": "208",
    "210": "208",
}
property_list = {
    "Attack": "AttackAddedRatio",
    "MaxHP": "HPAddedRatio",
    "Defence": "DefenceAddedRatio",
    "StatusResistance": "StatusResistanceBase",
    "Speed": "SpeedDelta",
    "BreakUp": "BreakDamageAddedRatioBase",
}


def save_weapon(weapon_dict):
    # map/EquipmentID2AbilityProperty
    EquipmentID2AbilityProperty = {}
    properties = {}
    for rank in range(0, 5):
        propertie = []
        if len(weapon_dict["data"]["skill"]["list"]) > 0:
            for index, propertiename in enumerate(weapon_dict["data"]["skill"]["list"]):
                propertieinfo = {}
                propertieinfo["PropertyType"] = propertiename
                propertieinfo["Value"] = {}
                propertieinfo["Value"]["Value"] = weapon_dict["data"]["skill"][
                    "params"
                ][str(index + 1)][rank]
                propertie.append(propertieinfo)
        properties[str(rank + 1)] = propertie
    EquipmentID2AbilityProperty[str(weapon_dict["data"]["id"])] = properties
    with open(
        gen_map_path / f"EquipmentID2AbilityProperty_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(EquipmentID2AbilityProperty)
    with open(
        gen_map_path / f"EquipmentID2AbilityProperty_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/EquipmentID2EnName
    EquipmentID2EnName = {}
    EquipmentID2EnName[str(weapon_dict["data"]["id"])] = weapon_dict["data"][
        "route"
    ].replace(" ", "")
    with open(
        gen_map_path / f"EquipmentID2EnName_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(EquipmentID2EnName)
    with open(
        gen_map_path / f"EquipmentID2EnName_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/EquipmentID2Name
    EquipmentID2Name = {}
    EquipmentID2Name[str(weapon_dict["data"]["id"])] = weapon_dict["data"]["name"]
    with open(
        gen_map_path / f"EquipmentID2Name_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(EquipmentID2Name)
    with open(
        gen_map_path / f"EquipmentID2Name_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/EquipmentID2Rarity
    EquipmentID2Rarity = {}
    EquipmentID2Rarity[str(weapon_dict["data"]["id"])] = weapon_dict["data"]["rank"]
    with open(
        gen_map_path / f"EquipmentID2Rarity_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(EquipmentID2Rarity)
    with open(
        gen_map_path / f"EquipmentID2Rarity_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # excel/EquipmentPromotionConfig
    EquipmentPromotionConfig = {}
    EquipmentPromotion = {}
    for index, upgrade in enumerate(weapon_dict["data"]["upgrade"]):
        Promotion = {}
        Promotion["EquipmentID"] = weapon_dict["data"]["id"]
        Promotion["Promotion"] = index
        materials = []
        if upgrade["costItems"]:
            promoteslist = upgrade["costItems"].keys()
            for keyname in promoteslist:
                material = {}
                material["ItemID"] = int(keyname)
                material["ItemNum"] = upgrade["costItems"][keyname]
                materials.append(material)
        Promotion["PromotionCostList"] = materials
        Promotion["MaxLevel"] = upgrade["maxLevel"]
        if upgrade["playerLevelRequire"]:
            Promotion["PlayerLevelRequire"] = upgrade["playerLevelRequire"]
        else:
            Promotion["WorldLevelRequire"] = upgrade["worldLevelRequire"]
        Promotion["BaseAttack"] = {}
        Promotion["BaseAttackAdd"] = {}
        Promotion["BaseDefence"] = {}
        Promotion["BaseDefenceAdd"] = {}
        Promotion["BaseHP"] = {}
        Promotion["BaseHPAdd"] = {}
        Promotion["BaseAttack"]["Value"] = upgrade["skillBase"]["attackBase"]
        Promotion["BaseAttackAdd"]["Value"] = upgrade["skillAdd"]["attackAdd"]
        Promotion["BaseDefence"]["Value"] = upgrade["skillBase"]["defenceBase"]
        Promotion["BaseDefenceAdd"]["Value"] = upgrade["skillAdd"]["defenceAdd"]
        Promotion["BaseHP"]["Value"] = upgrade["skillBase"]["hPBase"]
        Promotion["BaseHPAdd"]["Value"] = upgrade["skillAdd"]["hPAdd"]
        EquipmentPromotion[index] = Promotion
    EquipmentPromotionConfig[str(weapon_dict["data"]["id"])] = EquipmentPromotion
    with open(Excel_path / "EquipmentPromotionConfig.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data.update(EquipmentPromotionConfig)
    with open(
        Path("output") / "excel" / "EquipmentPromotionConfig.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # excel/light_cone_ranks
    light_cone_ranks = {}
    light_cone = {}
    light_cone["id"] = str(weapon_dict["data"]["id"])
    light_cone["skill"] = weapon_dict["data"]["skill"]["name"]
    light_cone["desc"] = weapon_dict["data"]["skill"]["description"]
    light_cone_params = weapon_dict["data"]["skill"]["params"]
    params = []
    for index in range(0, 5):
        paraminfo = []
        for param in light_cone_params:
            paraminfo.append(light_cone_params[param][index])
        params.append(paraminfo)
    light_cone["params"] = params
    properties = []
    for rank in range(0, 5):
        propertie = []
        if len(weapon_dict["data"]["skill"]["list"]) > 0:
            for index, propertiename in enumerate(weapon_dict["data"]["skill"]["list"]):
                propertieinfo = {}
                propertieinfo["type"] = propertiename
                propertieinfo["value"] = weapon_dict["data"]["skill"]["params"][
                    str(index + 1)
                ][rank]
                propertie.append(propertieinfo)
        properties.append(propertie)
    light_cone["properties"] = properties
    light_cone_ranks[str(weapon_dict["data"]["id"])] = light_cone
    with open(
        StarRailRes_path / "index_new/cn/light_cone_ranks.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(light_cone_ranks)
    with open(
        Path("output") / "excel" / "light_cone_ranks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_avatar(avatar_dict):
    # map/characterSkillTree
    mainSkills = avatar_dict["data"]["traces"]["mainSkills"]
    subSkills = avatar_dict["data"]["traces"]["subSkills"]
    characterSkillTree = {}
    Skilltree = {}
    for item in mainSkills:
        mainSkillid = mainSkills[item]["id"]
        mainskill = {}
        mainskill["id"] = str(mainSkills[item]["id"])
        mainskill["name"] = ""
        mainskill["max_level"] = mainSkills[item]["maxLevel"]
        mainskill["desc"] = ""
        mainskill["params"] = []
        mainskill["anchor"] = mainSkills[item]["pointPosition"]
        mainskill["pre_points"] = []
        level_up_skills = []
        icon_name = ""
        for skillid in mainSkills[item]["skillList"]:
            up_skills = {}
            up_skills["id"] = skillid
            up_skills["num"] = 1
            level_up_skills.append(up_skills)
            if mainSkills[item]["skillList"][skillid]["type"] == "普攻":
                icon_name = (
                    "icon/skill/" + str(avatar_dict["data"]["id"]) + "_basic_atk.png"
                )
            elif mainSkills[item]["skillList"][skillid]["type"] == "战技":
                icon_name = (
                    "icon/skill/" + str(avatar_dict["data"]["id"]) + "_skill.png"
                )
            elif mainSkills[item]["skillList"][skillid]["type"] == "终结技":
                icon_name = (
                    "icon/skill/" + str(avatar_dict["data"]["id"]) + "_ultimate.png"
                )
            elif mainSkills[item]["skillList"][skillid]["type"] == "天赋":
                icon_name = (
                    "icon/skill/" + str(avatar_dict["data"]["id"]) + "_talent.png"
                )
            elif mainSkills[item]["skillList"][skillid]["type"] == "秘技":
                icon_name = (
                    "icon/skill/" + str(avatar_dict["data"]["id"]) + "_technique.png"
                )
        mainskill["level_up_skills"] = level_up_skills
        levels = []
        for promotes in mainSkills[item]["promote"]:
            level = {}
            level["promotion"] = int(promotes) - 1
            level["level"] = 0
            level["properties"] = []
            materials = []
            if mainSkills[item]["promote"][promotes]["costItems"]:
                promoteslist = mainSkills[item]["promote"][promotes]["costItems"].keys()
                for keyname in promoteslist:
                    material = {}
                    material["id"] = str(keyname)
                    material["num"] = mainSkills[item]["promote"][promotes][
                        "costItems"
                    ][keyname]
                    materials.append(material)
            level["materials"] = materials
            levels.append(level)
        mainskill["levels"] = levels
        mainskill["icon"] = icon_name
        Skilltree[mainSkillid] = mainskill
    for item in subSkills:
        subSkillid = subSkills[item]["id"]
        subSkill = {}
        subSkill["id"] = str(subSkills[item]["id"])
        subSkill["name"] = subSkills[item]["name"]
        subSkill["max_level"] = subSkills[item]["maxLevel"]
        subSkill["desc"] = (
            subSkills[item]["description"] if subSkills[item]["description"] else ""
        )
        params = []
        if subSkills[item]["params"]:
            for param in subSkills[item]["params"]:
                params.append(subSkills[item]["params"][param])
        subSkill["params"] = params
        subSkill["anchor"] = subSkills[item]["pointPosition"]
        pre_points = pre_points_list.get(str(subSkillid)[-3:], 0)
        if pre_points != 0:
            pre_points = str(avatar_dict["data"]["id"]) + str(pre_points)
            subSkill["pre_points"] = [pre_points]
        else:
            subSkill["pre_points"] = []
        subSkill["level_up_skills"] = []
        levels = []
        for promotes in subSkills[item]["promote"]:
            level = {}
            level["promotion"] = (
                subSkills[item]["avatarPromotionLimit"]
                if subSkills[item]["avatarPromotionLimit"]
                else 0
            )
            level["level"] = 0
            properties = []
            if subSkills[item]["statusList"]:
                for status in subSkills[item]["statusList"]:
                    propertie = {}
                    if str(status["icon"])[4:] in property_list.keys():
                        typename = property_list[str(status["icon"])[4:]]
                    else:
                        typename = str(status["icon"])[4:]
                    propertie["type"] = typename
                    propertie["value"] = status["value"]
                    properties.append(propertie)
            level["properties"] = properties
            materials = []
            if subSkills[item]["promote"][promotes]["costItems"]:
                promoteslist = subSkills[item]["promote"][promotes]["costItems"].keys()
                for keyname in promoteslist:
                    material = {}
                    material["id"] = str(keyname)
                    material["num"] = subSkills[item]["promote"][promotes]["costItems"][
                        keyname
                    ]
                    materials.append(material)
            level["materials"] = materials
            levels.append(level)
        subSkill["levels"] = levels
        subSkill["icon"] = "icon/property/" + str(subSkills[item]["icon"]) + ".png"
        Skilltree[subSkillid] = subSkill
    characterSkillTree[str(avatar_dict["data"]["id"])] = Skilltree
    with open(
        gen_map_path / f"characterSkillTree_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(characterSkillTree)
    with open(
        gen_map_path / f"characterSkillTree_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarId2DamageType
    avatarId2DamageType = {}
    avatarId2DamageType[str(avatar_dict["data"]["id"])] = avatar_dict["data"]["types"][
        "combatType"
    ]["id"]
    with open(
        gen_map_path / f"avatarId2DamageType_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(avatarId2DamageType)
    with open(
        gen_map_path / f"avatarId2DamageType_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarId2EnName
    avatarId2EnName = {}
    avatarId2EnName[str(avatar_dict["data"]["id"])] = avatar_dict["data"]["route"]
    with open(
        gen_map_path / f"avatarId2EnName_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(avatarId2EnName)
    with open(
        gen_map_path / f"avatarId2EnName_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarId2Name
    avatarId2Name = {}
    avatarId2Name[str(avatar_dict["data"]["id"])] = avatar_dict["data"]["name"]
    with open(
        gen_map_path / f"avatarId2Name_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(avatarId2Name)
    with open(
        gen_map_path / f"avatarId2Name_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarId2Rarity
    avatarId2Rarity = {}
    avatarId2Rarity[str(avatar_dict["data"]["id"])] = str(avatar_dict["data"]["rank"])
    with open(
        gen_map_path / f"avatarId2Rarity_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(avatarId2Rarity)
    with open(
        gen_map_path / f"avatarId2Rarity_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarId2Star
    avatarId2Star = {}
    avatarId2Star[str(avatar_dict["data"]["id"])] = str(avatar_dict["data"]["rank"])
    with open(
        gen_map_path / f"avatarId2Star_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(avatarId2Star)
    with open(
        gen_map_path / f"avatarId2Star_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/avatarRankSkillUp
    avatarRankSkillUp = {}
    RankSkilllist = avatar_dict["data"]["eidolons"]
    for rankid in RankSkilllist:
        rankskillup = []
        if avatar_dict["data"]["eidolons"][rankid]["skillAddLevelList"]:
            for skillAddLevel in avatar_dict["data"]["eidolons"][rankid][
                "skillAddLevelList"
            ]:
                skilladd = {}
                skilladd["id"] = str(skillAddLevel)
                skilladd["num"] = avatar_dict["data"]["eidolons"][rankid][
                    "skillAddLevelList"
                ][skillAddLevel]
                rankskillup.append(skilladd)
        avatarRankSkillUp[rankid] = rankskillup
    with open(
        gen_map_path / f"avatarRankSkillUp_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(avatarRankSkillUp)
    with open(
        gen_map_path / f"avatarRankSkillUp_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # excel/AvatarPromotionConfig
    AvatarPromotionConfig = {}
    AvatarPromotion = {}
    for index, upgrade in enumerate(avatar_dict["data"]["upgrade"]):
        Promotion = {}
        Promotion["AvatarID"] = avatar_dict["data"]["id"]
        Promotion["Promotion"] = index
        materials = []
        if upgrade["costItems"]:
            promoteslist = upgrade["costItems"].keys()
            for keyname in promoteslist:
                material = {}
                material["ItemID"] = int(keyname)
                material["ItemNum"] = upgrade["costItems"][keyname]
                materials.append(material)
        Promotion["PromotionCostList"] = materials
        Promotion["MaxLevel"] = upgrade["maxLevel"]
        if upgrade["playerLevelRequire"]:
            Promotion["PlayerLevelRequire"] = upgrade["playerLevelRequire"]
        else:
            Promotion["WorldLevelRequire"] = upgrade["worldLevelRequire"]
        Promotion["AttackBase"] = {}
        Promotion["AttackAdd"] = {}
        Promotion["DefenceBase"] = {}
        Promotion["DefenceAdd"] = {}
        Promotion["HPBase"] = {}
        Promotion["HPAdd"] = {}
        Promotion["SpeedBase"] = {}
        Promotion["CriticalChance"] = {}
        Promotion["CriticalDamage"] = {}
        Promotion["BaseAggro"] = {}
        Promotion["AttackBase"]["Value"] = upgrade["skillBase"]["attackBase"]
        Promotion["AttackAdd"]["Value"] = upgrade["skillAdd"]["attackAdd"]
        Promotion["DefenceBase"]["Value"] = upgrade["skillBase"]["defenceBase"]
        Promotion["DefenceAdd"]["Value"] = upgrade["skillAdd"]["defenceAdd"]
        Promotion["HPBase"]["Value"] = upgrade["skillBase"]["hPBase"]
        Promotion["HPAdd"]["Value"] = upgrade["skillAdd"]["hPAdd"]
        Promotion["SpeedBase"]["Value"] = upgrade["skillBase"]["speedBase"]
        Promotion["CriticalChance"]["Value"] = upgrade["skillBase"]["criticalChance"]
        Promotion["CriticalDamage"]["Value"] = upgrade["skillBase"]["criticalDamage"]
        Promotion["BaseAggro"]["Value"] = upgrade["skillBase"]["baseAggro"]
        AvatarPromotion[index] = Promotion
    AvatarPromotionConfig[str(avatar_dict["data"]["id"])] = AvatarPromotion

    with open(Excel_path / "AvatarPromotionConfig.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data.update(AvatarPromotionConfig)
    with open(
        Path("output") / "excel" / "AvatarPromotionConfig.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/skillId2AttackType
    skillId2AttackType = {}
    for item in mainSkills:
        for skillid in mainSkills[item]["skillList"]:
            skillId2AttackType[skillid] = (
                mainSkills[item]["skillList"][skillid]["attackType"]
                if mainSkills[item]["skillList"][skillid]["attackType"]
                else ""
            )
    with open(
        gen_map_path / f"skillId2AttackType_mapping_{version}.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)
    data.update(skillId2AttackType)
    with open(
        gen_map_path / f"skillId2AttackType_mapping_{version}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/skillId2Name
    skillId2Name = {}
    for item in mainSkills:
        for skillid in mainSkills[item]["skillList"]:
            skillId2Name[skillid] = (
                mainSkills[item]["skillList"][skillid]["name"]
                if mainSkills[item]["skillList"][skillid]["name"]
                else ""
            )
    with open(
        gen_map_path / f"skillId2Name_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(skillId2Name)
    with open(
        gen_map_path / f"skillId2Name_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/skillId2Type
    skillId2Type = {}
    for item in mainSkills:
        for skillid in mainSkills[item]["skillList"]:
            skillId2Type[skillid] = (
                mainSkills[item]["skillList"][skillid]["tag"]
                if mainSkills[item]["skillList"][skillid]["tag"]
                else ""
            )
    with open(
        gen_map_path / f"skillId2Type_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(skillId2Type)
    with open(
        gen_map_path / f"skillId2Type_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # map/rankId2Name
    rankId2Name = {}
    for rankid in avatar_dict["data"]["eidolons"]:
        rankId2Name[rankid] = avatar_dict["data"]["eidolons"][rankid]["name"]
        # avatarRankSkillUp[rankid] = rankskillup
    with open(
        gen_map_path / f"rankId2Name_mapping_{version}.json", "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    data.update(rankId2Name)
    with open(
        gen_map_path / f"rankId2Name_mapping_{version}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def gen_beta_mapping(beta_json: Path):
    beta_avatar_json_list = list((beta_json / "avatar").iterdir())
    beta_equipment_json_list = list((beta_json / "equipment").iterdir())

    for beta_avatar_json in beta_avatar_json_list:
        with Path.open(beta_avatar_json, encoding="utf-8") as f:
            avatar_dict = json.load(f)
        save_avatar(avatar_dict)
    for beta_equipment_json in beta_equipment_json_list:
        with Path.open(beta_equipment_json, encoding="utf-8") as f:
            weapon_dict = json.load(f)
        save_weapon(weapon_dict)

    # test
    import test.SR_MAP_PATH as sr_map  # noqa: F401
    import model as excel_model  # noqa: F401


# if __name__ == "__main__":
#     gen_beta_mapping()
