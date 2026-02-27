from .models.c6bank.c6bank import C6bankMapper
from .banksRobot.C6_Bank import C6_Bank

factoryBanksMapper = {
    "c6bank": C6bankMapper(),
}

factoryBanks = {
    "c6bank": C6_Bank(),
}