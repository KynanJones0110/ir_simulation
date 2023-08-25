# IR_Simulation
My API-less version of AttackGen (https://attackgen.streamlit.app/) as opposed to utilising ChatGPT's API, it will print the output to screen for manual input into Chat-GPT.


```
pip install mitreattack-python
pip install mitreattack
```




The dataset enterprise-attack.json (https://github.com/mitre/cti/blob/master/enterprise-attack/enterprise-attack.json) will need to be downloaded and imported into your project/repo.

If the path needs to be modified, head to the load_attack_data function and change the value passed to the MitreAttackData function.

def load_attack_data():
    attack_data = MitreAttackData("%YOUR PATH%enterprise-attack.json")
    return attack_data

  To do / Potentially:
  - Further testing in GPT for best prompt
  - Output file to text?
  - Create an alternative for threat hunting

    
