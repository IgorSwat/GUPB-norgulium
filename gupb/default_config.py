from gupb.controller import keyboard
from gupb.controller import random
from gupb.controller.camperbot import camperbot
from gupb.controller.neat import kim_dzong_neat_jr
from gupb.controller import kirby_learning
from gupb.controller.norgul import norgul
from gupb.controller import reinforced_rogue
from gupb.controller import garek
from gupb.controller import rustler
from gupb.controller.bupg import bupg
from gupb.controller.pirat import pirat
from gupb.controller import roomba
from gupb.controller import Keramzytowy_mocarz


keyboard_controller = keyboard.KeyboardController()

CONFIGURATION = {
    'arenas': [
        'ordinary_chaos',
        # 'isolated_shrine'
    ],
    'controllers': [
        random.RandomController("Alice"),
        camperbot.CamperBotController("Camper"),
        kim_dzong_neat_jr.KimDzongNeatJuniorController(),
        kirby_learning.KirbyLearningController("KirbyLearning"),
        norgul.NorgulController("Norgul"),
        # reinforced_rogue.ReinforcedRogueController("ReinforcedRogue"),
        # garek.GarekController("Garek"),
        # rustler.Rustler("Rustler"),
        # bupg.BUPGController("BUPG"),
        # roomba.RoombaController("Roomba"),
        # pirat.PiratController("Pirat"),
        # Keramzytowy_mocarz.Keramzytowy_mocarz("KERAMZYTOWY_MOCARZ"),
    ],
    'start_balancing': False,
    'visualise': True,
    'show_sight': True,
    'runs_no': 1,
    'profiling_metrics': [],
}

