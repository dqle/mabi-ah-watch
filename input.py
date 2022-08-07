### Format:
###   name
###   url
###   alert price

def itemList():
    watchList = [
        [
            "Abyssal Orb",
            "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%225100032%22&sort=ItemPrice%3AAscending&page=0",
            "70000000"
        ],
        [
            "Blazing Flame",
            "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemName%2C%22Blazing+Flame%22%3BItemId%2Ceq%2C%225100034%22&sort=ItemPrice%3AAscending&page=0",
            "60000000"
        ],
        [
            "Hayashi Boots",
            "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%2217772%22&sort=ItemName%3AAscending&page=0",
            "2000000"
        ],
        [
            "Glowing Mask",
            "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%22221081%22&sort=ItemName%3AAscending&page=0",
            "40000000"
        ],
        [
            "Mysterious Shard",
            "https://na.mabibase.com/tools/auction-house?server=mabius6&q=ItemId%2Ceq%2C%2264108%22&sort=ItemPrice%3AAscending&page=0",
            "2000000"
        ]
    ]

    return watchList

def discordURL():
    URL="enter discord webhook url here"
    return URL