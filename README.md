# INCOMPLETE

# Deps
1. Install pygame `pip3 install pygame`
2. Go to the terminal and run `python3 Main.py`

# 필독
코드 작성 환경 : Linux(Ubuntu 22.04 TLS)


macOS 사용하는 경우에는 변경 필요 X


windows를 사용할 경우에는 파일 경로들을 / 에서 \\\\ 로 바꿔야 함
```
"images/background.png" // linux, macOS version
"images\\background.png" //windows version
```

# Audios
## How to get Audios Free
Use the following site, [here](https://www.chosic.com/free-music/games/)

`Main.py`의 `pygame.mixer.music.load("audio/Luke-Bergs-Bliss(chosic.com).mp3")`를 원하는 오디오로 바꿔주면 됨.

`audio` 파일에 새로운 오디오를 추가하면 됨.

# Fonts
`Main.py` 의 `leaderboard_font`, `username_font`를 원하는 폰트로 바꿔주면 됨.

폰트들은 `fonts` 파일에 있음. (Jumpking에서 가져온 폰트들, 출처 한 번 확인해 볼 것.)

# `LampRenderer.py`
램프의 밝기를 설정해 주기 위한 모듈로, 제출 전에는 삭제하고 낼 것 (!!!)

# Differences with the implementation Guide
구현 스펙과 상이한 부분들이 있는데, 
1. 스테이지의 도입
높이 올라간다는 성질을 스테이지가 증가하는 것으로 표현했고, 각 스테이지가 연속적으로 이어지도록 배경 블록의 아래 두 행이 전의 스테이지의 위 두 행과 일치하도록 구현함.
스테이지가 올라갈수록 램프의 밝기가 증가하게 됨. 만약 램프 사진을 수정하고 싶으면, `LampRenderer.py`를 이용해서 Base Lamp의 밝기를 올려주면 끝.
2. 담쟁이의 성질
일단 기본적으로 담쟁이가 `Player`를 향해서 자라는데, 담쟁이도 블록처럼 밟고 올라갈 수 있게 구현함(안 그러면 게임이 너무 깨기 어려워져서)
또한, 희망 스킬을 쓰면 담쟁이가 쭉 자라면서 스테이지 하나를 완전히 깨게 해 줌.

# Game Guide
1. 처음에 사용자명을 입력
2. 리더보드 창이 나옴(`pickle` 사용)
3. 왼, 오, 위 화살표로 움직일 수 있음
4. 희망 스킬 사용은 스페이스바 누르면 됨(게이지 안 찬 상태에서는 사용불가능)
5. 게임 오버는 미구현, 리더보드를 위해서 미구현하는게 맞는듯... 만약 구현한다면 어떻게 하면 좋을지 한번 생각해보면 될듯.
