# Defining some functions

def bet_ratio(odds1, odds2):
    'Function assumes inputs give arbitrage'
    'This function will return how much to bet on each odds per $100 to maximise return'
    max_return = 0
    i = 0.0001
    while i <= 0.9999:
        if (odds1*i - 1) and (odds2*(1 - i) - 1) > max_return:
            max_return = min(odds1*i - 1, odds2*(1 - i) - 1)
            odds1ratio = i
            odds2ratio = 1 - i
        i += 0.0001
    return [odds1ratio, odds2ratio]

def odds_arbitrage(data1, data2):
    'data takes form [bookmaker, [team1, oddswin1], [team2, oddswin2]]'
    'This function returns either no arbitrage available or returns an arbitrage bet'
    BookmakerA = data1[0]
    BookmakerB = data2[0]

    if 1/float(data1[1][1]) + 1/float(data2[2][1]) < 1:
        BookmakerA_ArbOdds = float(data1[1][1])
        BookmakerB_ArbOdds = float(data2[2][1])
        BookmakerA_team = data1[1][0]
        BookmakerB_team = data2[2][0]

    if 1/float(data1[2][1]) + 1/float(data2[1][1]) < 1:
        BookmakerA_ArbOdds = float(data1[2][1])
        BookmakerB_ArbOdds = float(data2[1][1])
        BookmakerA_team = data1[2][0]
        BookmakerB_team = data2[1][0]

    else:
        return 'No arbitrage available'

    arbitrage_odds = bet_ratio(BookmakerA_ArbOdds, BookmakerB_ArbOdds)

    return 'Bet ' + str(round(arbitrage_odds[0], 4)) + ' on ' + BookmakerA_team + ' ' + str(BookmakerA) +'\n' + 'Bet ' + str(round(arbitrage_odds[1], 4)) + ' on ' + BookmakerB_team + ' ' + str(BookmakerB)
