"""The template of the main script of the machine learning processs"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop():
    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    aid = 0
    past_ball_position = []
    ball_down = False
    
    # 3. Start an endlless loop.
    while True:
        # 3.1. Receive the scene infromation sent from the game process.
        scene_info = comm.get_scene_info()
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
            
        # 3.3. Put the code gere to handle the scene information
        now_ball_position = scene_info.ball
        if len(past_ball_position) == 0:
            past_ball_position = now_ball_position
        else:
            if (now_ball_position[1] - past_ball_position[1]) > 0:
                ball_down = True
            else:
                ball_down = False
            
            if (now_ball_position[0] - past_ball_position[0]) > 0:
                ball_right = True
            else:
                ball_right = False
                
        now_platform_positionX = scene_info.platform[0] + 20
        print(now_platform_positionX , now_ball_position)
        if ball_down == True and now_ball_position[1] > 280:
            m = (now_ball_position[1] - past_ball_position[1]) / (now_ball_position[0] - past_ball_position[0])
            res = now_ball_position[0] - ((now_ball_position[1] - 395) / m)
            if res < 0:
                res = -res
            elif res > 200:
                res = 200 - (res - 200)
        else:
            res = 100
            
        if ball_down == False and now_ball_position[1] > 280:
            if now_ball_position[0] > 150:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif now_ball_position[0] < 50:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                if now_platform_positionX > 140:
                    if now_ball_position[0] > now_platform_positionX + 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if now_ball_position[0] < now_platform_positionX + 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif 140 > now_platform_positionX > 100:
                    if now_ball_position[0] > now_platform_positionX + 10:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if now_ball_position[0] < now_platform_positionX + 10:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif 100 > now_platform_positionX > 60:
                    if now_ball_position[0] > now_platform_positionX - 10:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if now_ball_position[0] < now_platform_positionX - 10:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    if now_ball_position[0] > now_platform_positionX - 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if now_ball_position[0] < now_platform_positionX - 20:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            if res > now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            if res < now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if res == now_platform_positionX:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            
        past_ball_position = now_ball_position