# beamdbg
[esolang Beam](https://esolangs.org/wiki/Beam)으로 개발하는 프로그래머들을 위한 디버거입니다!!  
[CTF 문제](https://dreamhack.io/wargame/challenges/940)를 풀다가 생긴 흥미가 여기까지 오게 되었습니다...  

GDB를 모방해서 만들었고, Beam 언어의 특성에 맞게 조금 수정되었습니다.  
디버거의 기본적인 기능을 대부분 갖추고 있습니다.  

## 사용법
Beam 프로그래밍에 대한 이해가 적으시다면, 
[Beam wiki](https://esolangs.org/wiki/Beam)를 먼저 보고 오시길 추천드립니다.  

### 다운로드
```shell
cd ~
git clone https://github.com/h0pler/beamdbg.git
cd beamdbg
```  

### 실행 방법
*코드 파일*, *입력 파일*, *출력 파일*을 먼저 생성하신 후 진행하셔야 합니다.  
입력과 출력이 따로 없는 코드여도, 꼭 생성 후 실행하셔야 합니다.  
`python main.py <code> <input> <output>`  
### 명령어
- **start** : code, input 파일을 읽어와 Beam 프로세스를 시작합니다.
- **ni \<steps\>** : Next Instruction의 축약어로, `steps`가 제공되지 않았다면 1만큼, 제공되었다면 `steps`만큼 실행합니다. 실행 중 breakpoint를 만날 경우 실행이 중단됩니다.
- **b \[x\] \[y\]** : Breakpoint의 축약어로, 코드의 `x`행 `y`열에 breakpoint를 생성합니다.
- **run** : 프로세스를 끝까지 실행합니다. 실행 중 breakpoint를 만날 경우 실행이 중단됩니다.
- **mem** : 프로세스의 현재 메모리 상태를 표시합니다.
- **exit/quit** : beamdbg를 종료합니다.
- **help** : 도움말을 표시합니다.  


---
---

프로젝트에 개선점이나 문제점이 발견되면 Issue나 Pull request 자유롭게 부탁드립니다!  
재밌으셨다면 스타 하나만 찍어주세용..ㅎㅎ  