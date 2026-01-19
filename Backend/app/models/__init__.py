from .aki import Aki
from .amigoz import Amigoz
from .brb360 import Brb360
from .brbInconta import Brbinconta
from .btw import Btw
from .bv import bv
from .c6auto import c6auto
from .c6bankcreditomanual import c6bankcreditomanual
from .c6bankcomissao import c6bankcomissao
from .c6bankdebitomanual import c6bankdebitomanual
from .c6equity import c6equity
from .caixa import caixa
from .crefisa import crefisa
from .digio import digio
from .empresteicred import empresteicred
from .euro import euro
from .evol import evol
from .facta import facta
from .grandino import grandino
from .happy import happy
from .hope import hope
from .icred import icred
from .jbcred import jbcred
from .kardbank import kardbank
from .nbc import nbc
from .neo import neo
from .novosaque import novosaque
from .novosaquecartao import novosaquecartao
from .nyc import nyc
from .paranabank import paranabank
from .phtech import phtech
from .presenca import presenca
from .qualibank import qualibank
from .queromaiscancelados import queromaiscancelados
from .queromaiscomissao import queromaiscomisssao
from .queromaisseguro import queromaisseguro
from .safracomissaozero import safracomissaozero
from .santanderfit import santanderfit
from .santanderFve6 import santanderfvevi
from .santanderolewl import santanderolewl
from .totalcash import totalcash
from .v8 import v8
from .vctex import vctex
from .webcash import webcash

bancos = {
    "aki": lambda df: Aki().run(df),
    "amigoz": lambda df: Amigoz().run(df),
    "brb360": lambda df: Brb360().run(df),
    "brbinconta": lambda df: Brbinconta().run(df),
    "btw": lambda df: Btw().run(df),
    "bv": bv,
    "c6auto": c6auto,
    "c6bankcreditomanual": c6bankcreditomanual,
    "c6bankcomissao": c6bankcomissao,
    "c6bankdebitomanual": c6bankdebitomanual,
    "c6equity": c6equity,
    "caixa": caixa,
    "crefisa": crefisa,
    "digio": digio,
    "empresteicred": empresteicred,
    "euro": euro,
    "evol": evol,
    "facta": facta,
    "grandino": grandino,
    "happy": happy,
    "hope": hope,
    "icred": icred,
    "jbcred": jbcred,
    "kardbank": kardbank,
    "nbc": nbc,
    "neo": neo,
    "novosaque": novosaque,
    "novosaquecartao": novosaquecartao,
    "nyc": nyc,
    "paranabank": paranabank,
    "phtech": phtech,
    "presenca": presenca,
    "qualibank": qualibank,
    "queromaiscancelados": queromaiscancelados,
    "queromaiscomissao": queromaiscomisssao,
    "queromaisseguro": queromaisseguro,
    "safracomissaozero": safracomissaozero,
    "santanderfit": santanderfit,
    "santanderfvevi": santanderfvevi,
    "santanderolewl": santanderolewl,
    "totalcash": totalcash,
    "v8": v8,
    "vctex": vctex,
    "webcash": webcash
}