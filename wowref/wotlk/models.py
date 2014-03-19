from django.db import models


class ItemTemplate(models.Model):
    entry = models.AutoField(primary_key=True)
    class_field = models.IntegerField(db_column='class')
    sub_class = models.IntegerField(db_column='subclass')
    name = models.CharField(max_length=255)
    display_id = models.IntegerField(db_column="displayid")
    quality = models.IntegerField(db_column='Quality')
    flags = models.IntegerField(db_column='Flags')
    flags_extra = models.IntegerField(db_column='FlagsExtra')
    buy_count = models.IntegerField(db_column='BuyCount')
    buy_price = models.BigIntegerField(db_column='BuyPrice')
    sell_price = models.IntegerField(db_column='SellPrice')
    inv_type_id = models.IntegerField(db_column='InventoryType')
    allowable_class = models.IntegerField(db_column='AllowableClass')
    allowable_race = models.IntegerField(db_column='AllowableRace')
    item_level = models.IntegerField(db_column='ItemLevel')
    required_level = models.IntegerField(db_column='RequiredLevel')
    required_skill = models.IntegerField(db_column='RequiredSkill')
    required_skill_rank = models.IntegerField(db_column='RequiredSkillRank')
    requiredspell = models.IntegerField()
    requiredhonorrank = models.IntegerField()
    required_city_rank = models.IntegerField(db_column='RequiredCityRank')
    required_reputation_faction = models.IntegerField(db_column='RequiredReputationFaction')
    required_reputation_rank = models.IntegerField(db_column='RequiredReputationRank')
    maxcount = models.IntegerField()
    stackable = models.IntegerField(null=True, blank=True)
    container_slots = models.IntegerField(db_column='ContainerSlots')
    stats_count = models.IntegerField(db_column='StatsCount')
    stat_type1 = models.IntegerField()
    stat_value1 = models.IntegerField()
    stat_type2 = models.IntegerField()
    stat_value2 = models.IntegerField()
    stat_type3 = models.IntegerField()
    stat_value3 = models.IntegerField()
    stat_type4 = models.IntegerField()
    stat_value4 = models.IntegerField()
    stat_type5 = models.IntegerField()
    stat_value5 = models.IntegerField()
    stat_type6 = models.IntegerField()
    stat_value6 = models.IntegerField()
    stat_type7 = models.IntegerField()
    stat_value7 = models.IntegerField()
    stat_type8 = models.IntegerField()
    stat_value8 = models.IntegerField()
    stat_type9 = models.IntegerField()
    stat_value9 = models.IntegerField()
    stat_type10 = models.IntegerField()
    stat_value10 = models.IntegerField()
    scaling_stat_distribution = models.IntegerField(db_column='ScalingStatDistribution')
    scaling_stat_value = models.IntegerField(db_column='ScalingStatValue')
    dmg_min1 = models.FloatField()
    dmg_max1 = models.FloatField()
    dmg_type1 = models.IntegerField()
    dmg_min2 = models.FloatField()
    dmg_max2 = models.FloatField()
    dmg_type2 = models.IntegerField()
    armor = models.IntegerField()
    holy_res = models.IntegerField()
    fire_res = models.IntegerField()
    nature_res = models.IntegerField()
    frost_res = models.IntegerField()
    shadow_res = models.IntegerField()
    arcane_res = models.IntegerField()
    delay = models.IntegerField()
    ammo_type = models.IntegerField()
    ranged_mod_range = models.FloatField(db_column='RangedModRange')
    spell_id_1 = models.IntegerField(db_column="spellid_1")
    spell_trigger_1 = models.IntegerField(db_column="spelltrigger_1")
    spell_charges_1 = models.IntegerField(db_column="spellcharges_1", null=True, blank=True)
    spell_ppm_rate_1 = models.FloatField(db_column='spellppmRate_1')
    spell_cooldown_1 = models.IntegerField(db_column="spellcooldown_1")
    spell_category_1 = models.IntegerField(db_column="spellcategory_1")
    spell_category_cooldown_1 = models.IntegerField(db_column="spellcategorycooldown_1")
    spell_id_2 = models.IntegerField(db_column="spellid_2")
    spell_trigger_2 = models.IntegerField(db_column="spelltrigger_2")
    spell_charges_2 = models.IntegerField(db_column="spellcharges_2", null=True, blank=True)
    spell_ppm_rate_2 = models.FloatField(db_column='spellppmRate_2')
    spell_cooldown_2 = models.IntegerField(db_column="spellcooldown_2")
    spell_category_2 = models.IntegerField(db_column="spellcategory_2")
    spell_category_cooldown_2 = models.IntegerField(db_column="spellcategorycooldown_2")
    spell_id_3 = models.IntegerField(db_column="spellid_3")
    spell_trigger_3 = models.IntegerField(db_column="spelltrigger_3")
    spell_charges_3 = models.IntegerField(db_column="spellcharges_3", null=True, blank=True)
    spell_ppm_rate_3 = models.FloatField(db_column='spellppmRate_3')
    spell_cooldown_3 = models.IntegerField(db_column="spellcooldown_3")
    spell_category_3 = models.IntegerField(db_column="spellcategory_3")
    spell_category_cooldown_3 = models.IntegerField(db_column="spellcategorycooldown_3")
    spell_id_4 = models.IntegerField(db_column="spellid_4")
    spell_trigger_4 = models.IntegerField(db_column="spelltrigger_4")
    spell_charges_4 = models.IntegerField(db_column="spellcharges_4", null=True, blank=True)
    spell_ppm_rate_4 = models.FloatField(db_column='spellppmRate_4')
    spell_cooldown_4 = models.IntegerField(db_column="spellcooldown_4")
    spell_category_4 = models.IntegerField(db_column="spellcategory_4")
    spell_category_cooldown_4 = models.IntegerField(db_column="spellcategorycooldown_4")
    spell_id_5 = models.IntegerField(db_column="spellid_5")
    spell_trigger_5 = models.IntegerField(db_column="spelltrigger_5")
    spell_charges_5 = models.IntegerField(db_column="spellcharges_5", null=True, blank=True)
    spell_ppm_rate_5 = models.FloatField(db_column='spellppmRate_5')
    spell_cooldown_5 = models.IntegerField(db_column="spellcooldown_5")
    spell_category_5 = models.IntegerField(db_column="spellcategory_5")
    spell_category_cooldown_5 = models.IntegerField(db_column="spellcategorycooldown_5")
    bonding = models.IntegerField()
    description = models.CharField(max_length=255)
    page_text = models.IntegerField(db_column='PageText')
    language_id = models.IntegerField(db_column='LanguageID')
    page_material = models.IntegerField(db_column='PageMaterial')
    startquest = models.IntegerField()
    lockid = models.IntegerField()
    material = models.IntegerField(db_column='Material')
    sheath = models.IntegerField()
    random_property = models.IntegerField(db_column='RandomProperty')
    random_suffix = models.IntegerField(db_column='RandomSuffix')
    block = models.IntegerField()
    item_set = models.IntegerField(db_column="itemset")
    max_durability = models.IntegerField(db_column='MaxDurability')
    area = models.IntegerField()
    map = models.IntegerField(db_column='Map')
    bag_family = models.IntegerField(db_column='BagFamily')
    totem_category = models.IntegerField(db_column='TotemCategory')
    socket_color_1 = models.IntegerField(db_column='socketColor_1')
    socket_content_1 = models.IntegerField(db_column='socketContent_1')
    socket_color_2 = models.IntegerField(db_column='socketColor_2')
    socket_content_2 = models.IntegerField(db_column='socketContent_2')
    socket_color_3 = models.IntegerField(db_column='socketColor_3')
    socket_content_3 = models.IntegerField(db_column='socketContent_3')
    socket_bonus = models.IntegerField(db_column='socketBonus')
    gem_properties = models.IntegerField(db_column='GemProperties')
    required_disenchant_skill = models.IntegerField(db_column='RequiredDisenchantSkill')
    armor_damage_modifier = models.FloatField(db_column='ArmorDamageModifier')
    duration = models.IntegerField()
    item_limit_category = models.IntegerField(db_column='ItemLimitCategory')
    holiday_id = models.IntegerField(db_column='HolidayId')
    script_name = models.CharField(max_length=64, db_column='ScriptName')
    disenchant_id = models.IntegerField(db_column='DisenchantID')
    food_type = models.IntegerField(db_column='FoodType')
    min_money_loot = models.IntegerField(db_column='minMoneyLoot')
    max_money_loot = models.IntegerField(db_column='maxMoneyLoot')
    wdb_verified = models.IntegerField(null=True, db_column='WDBVerified', blank=True)

    def __getitem__(self, key):
        return self.__dict__[key]

    class Meta:
        managed = False
        db_table = 'item_template'