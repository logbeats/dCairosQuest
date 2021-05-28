# dCairosQuest

클라우드 시스템 보안 RPA(Robotic Process Automation) dCairos 프로젝트 자동화 프로세스
(Cloud System security RPA(Robotic Process Automation) dCairos Project automation process)

보안 분석 업무 프로세스 자동화 기능 제공 - 추출, 데이터마이닝, 분류, 결과 등
(Provides security analysis work process automation function - Extraction, data mining, classification, results, etc.)

dCairos 프로젝트의 일부로 클라우드 서비스 환경에 따라 예제 변경 및 관리가 가능하여 단독으로 사용할 수 있습니다.
(It is a part of the dCairos project, and it can be used alone as it is possible to change and manage examples according to the cloud service environment.)


## 설치(Installation)
```
pip install -r requirements.txt
             or
pip3 install -r requirements.txt
```
### 요구 사항(Requirements)
  * Python 3.7+
  * Windows or Linux or MacOS:테스트 중(under testing)

### 실행 및 명령 줄 인터페이스(Run and Command-Line Interface)
`script` 디렉터리에는 OS 별 데이터 추출 스크립트가 포함되어 있습니다. 데이터는 명령 줄(CLI) 또는 실행을 통해서 얻습니다.(The directory contains OS-specific data extraction scripts. Data is obtained from the command line (CLI) or through execution)

* `Windows` - '.bat' 실행을 통해서 얻습니다.(It is obtained through execution)
* `Linux` - '.sh' 명령 줄(CLI)을 통해서 얻습니다.(Obtained through the command line (CLI))
* `MacOS` - '.sh' 현재 지원되지 않습니다.(Currently not supported)
* `확실한 결과를 얻으려면 관리자 권한으로 실행해야합니다.(You need to run it with administrator privileges to get definite results)`

## 사용법(Usage)
1. 추출 된 데이터를 `workspace\input` 디렉토리에 복사합니다.(Copy the extracted data to the `workspace\input` directory)
2. `workspace\input` 디렉터리가 없으면 새로 만들거나 dCairos.py를 실행합니다.(If the directory does not exist, create it or run dCairos.py)
   ```
    python dCairos.py
           or
    python3 dCairos.py
   ```
3. 아래와 같이`-d`의 인수 값을 입력하면 지정된 프로세스가 실행됩니다.(Entering the argument value of `-d` as shown below executes the specified process.)
   ```
    python dCairos.py -d
           or
    python3 dCairos.py -d
   ```
4. 실행이 완료되면 데이터 마이닝 / 분석 / 분류 등을 자동으로 수행하여 결과를 얻습니다.(Upon completion of execution, data mining/analysis/classification, etc. are automatically performed to obtain results)
   ![dCairosQuest](https://user-images.githubusercontent.com/46318494/119313293-57e6b180-bcae-11eb-8199-86c8070e6fc0.jpg)
5. 아래 표는 기본 디렉토리 구조를 보여줍니다.(The table below shows the main directory structure)
   Datawork|extraction|Classification|
   ----|----|----|
   workspace|script|conf|
   input|Linux|csv|
   output|MacOS|xlsx|
   project|Windows|cli|
6. dCairosQuest는 모듈 형태로 사용할 수 있습니다.(dCairosQuest can be used in modular form.)

## GUI 사용 예(GUI usage example)

![dCairos](https://user-images.githubusercontent.com/46318494/119974697-f09f6900-bfef-11eb-87b1-19eeb4dfca34.gif)