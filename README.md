# Risk Parity Optimizer
 
risk parity 전략의 objective funciton은 가장 흔하게 발견할 수 있는 function을 사용했다.

하지만 이 목적 함수는 convex 문제가 아니어서 수정이 필요하다.


## convex 문제가 아닐 경우 발생하는 문제

ositive directional derivative for linesearch
* https://stackoverflow.com/questions/11155721/positive-directional-derivative-for-linesearch

이 외에도 iteration 동안에 error를 minimize 하지 못해서 에러가 발생하기도 한다.
* https://stackoverflow.com/questions/57153111/scipy-optmize-minimize-iteration-limit-exceeded

이 문제를 해결하기 위해서는 목적함수를 변경해야한다. 확인 해본 결과 risk parity 전략은 다양한 목적함수가 존재한다.

## solution
목적함수를 convex 문제로 변경하는 방법은 다음 논문에 잘 나와있다.
* Constrained Risk Budgeting Portfolios Theory, Algorithms, Applications & Puzzles∗ Jean-Charles Richard, Thierry Roncalli, January 2019

목적함수를 convex 문제로 변경하면 cvxpy 라이브러리도 사용할 수 있을 것으로 보인다.

이 외에도 qlib에서 risk parity를 구현하는 방식도 참고하면 좋을 것 같다.

여기는 또 다른 목적함수를 사용하며 scipy 패키지를 사용하여 문제를 해결한다.
