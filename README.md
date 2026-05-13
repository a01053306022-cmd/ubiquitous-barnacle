<!-- 경영정보처리론 실습과제2 README -->

<div align="center">

# 🔥 공공데이터 시각화 대시보드

**경영정보처리론 실습과제 2**

![Badge](https://img.shields.io/badge/데이터출처-공공데이터포털-blue?style=flat-square)
![Badge](https://img.shields.io/badge/주제-화재현황-red?style=flat-square)
![Badge](https://img.shields.io/badge/학번-2514529-gray?style=flat-square)

> 2514529 이채영

</div>

---

## 📌 1. 사용한 프롬프트

🔗 [Google AI Studio 프롬프트 링크](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%2217SfllAT8Ye-sZgD4NO1OXvkFlM0gEsHd%22%5D,%22action%22:%22open%22,%22userId%22:%22106342282392641037287%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing)

---

## 📊 2. 데이터 및 시각화 결과 설명

### 🗂️ 사용 데이터

**소방청\_화재현황** ([공공데이터포털](https://www.data.go.kr/data/15155635/fileData.do))

총 57개 컬럼 중 아래 **13개 컬럼**을 선별하여 사용하였으며,
`접수일시`를 Key로 3개의 테이블로 분류·연결하였습니다.

<table>
  <thead>
    <tr>
      <th>분류</th>
      <th>사용 컬럼</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>🌡️ 온도 및 습도</td>
      <td><code>온도</code>, <code>습도</code></td>
    </tr>
    <tr>
      <td>💨 풍속 및 풍향</td>
      <td><code>풍속</code>, <code>풍향</code></td>
    </tr>
    <tr>
      <td>📋 기타 화재 정보</td>
      <td><code>인명피해(명)소계</code>, <code>사망</code>, <code>부상</code>, <code>재산피해소계(천원)</code>, <code>접수일시</code>, <code>발화층</code>, <code>화재유형</code>, <code>발화요인대분류</code>, <code>발화요인소분류</code></td>
    </tr>
  </tbody>
</table>

---

### 📈 시각화 주제 및 결과

> 화재 발생에 영향을 주는 **발화요인**, **계절**, **습도**를 중심으로 2개 그래프를,  
> 피해액 확대에 영향을 주는 **풍속**을 중심으로 1개 그래프를 작성하였습니다.

<br>

#### 🔥 그래프 1. 발화요인 대분류별 화재 발생 현황

<details>
<summary>결과 보기</summary>

<br>

- **부주의**로 인한 화재 발생이 압도적으로 많음을 확인할 수 있었습니다.
- **전기적 요인 / 기계적 요인** 순으로 발생 빈도가 높았습니다.
- → **부주의, 전기적·기계적 요인**을 예방하면 대부분의 화재를 막을 수 있을 것으로 예측됩니다.

</details>

<br>

#### 🌧️ 그래프 2. 계절별 습도 구간에 따른 화재 발생

<details>
<summary>결과 보기</summary>

<br>

- **겨울**에 화재 발생량이 가장 많았으며, 나머지 계절의 발생량은 비슷한 수준이었습니다.
- 계절과 무관하게 **습도 45~80% 구간**에서 화재가 가장 잦게 발생하는 것으로 나타났습니다.

</details>

<br>

#### 💸 그래프 3. 풍속 구간별 평균 재산 피해

<details>
<summary>결과 보기</summary>

<br>

- **풍속 18m/s 이상**일 때 평균 재산 피해액이 가장 높게 나타났습니다.
- 18m/s 미만 구간에서는 풍속에 따른 유의미한 재산 피해 차이가 관찰되지 않았습니다.

</details>

---

<div align="center">

*경영정보처리론 실습과제2 | 숙명여자대학교*

</div>
