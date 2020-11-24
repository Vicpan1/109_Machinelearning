"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import pickle
import numpy as np

def ml_loop():
    mode = "TestTrain" # TestTrain RuleBase
    predictFunction = "knn" #svm
    aid = 0
    past_ball_position = []
    ball_down = False
    comm.ml_ready()

    if mode == "RuleBase":
        while True:
            scene_info = comm.get_scene_info()

            if scene_info.status == GameStatus.GAME_OVER or \
                scene_info.status == GameStatus.GAME_PASS:
                comm.ml_ready()
                continue
            now_ball_position = scene_info.ball

            if len(past_ball_position) == 0:
                past_ball_position = now_ball_position
            else:
                if (now_ball_position[1] - past_ball_position[1]) > 0:
                    ball_down = True
                else:
                    ball_down = False
            now_platform_positionX = scene_info.platform[0] + 20

            if ball_down == True and now_ball_position[1] > 200:
                m = (now_ball_position[1] - past_ball_position[1]) / (now_ball_position[0] - past_ball_position[0])
                aid = now_ball_position[0] - ((now_ball_position[1] - 395) / m)
                if aid < 0:
                    aid = -aid
                elif aid > 200:
                    aid = 200 - (aid - 200)
            else:
                aid = 100

            if aid > now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            if aid < now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if aid == now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            past_ball_position = now_ball_position

    if mode == "TestTrain":   
        filename = predictFunction + ".sav"
        model = pickle.load(open(filename, 'rb')) 
        
        while True:
            scene_info = comm.get_scene_info()
            now_ball_position = scene_info.ball

            if len(past_ball_position) != 0:
                inp_temp = np.array([past_ball_position[0], past_ball_position[1], now_ball_position[0], now_ball_position[1], scene_info.platform[0]])
                input = inp_temp[np.newaxis, :]
                
                if scene_info.status == GameStatus.GAME_OVER or \
                    scene_info.status == GameStatus.GAME_PASS:
                    comm.ml_ready()
                    continue
                move = model.predict(input)

                if move < 0:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif move > 0:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)    
            past_ball_position = now_ball_position