from mitreattack.stix20 import MitreAttackData

#pip install mitreattack-python
#pip install mitreattack

# add in a guide, so if they want assistance it will break down the roles and responsibilities of different teams, 


def list_group():
        global selected_group_name
        attack_data = load_attack_data()
        groups = attack_data.get_groups(remove_revoked_deprecated=True)
        i = 1
        for group in groups:
            print("[" + str(i) + "] " + group.name)
            i += 1
        choice = int(input("Enter your APT of choice by number: "))
        selected_group = groups[choice - 1]
        selected_group_name = (selected_group.name)
        group = attack_data.get_groups_by_alias(selected_group_name)
        if group:
             group_stix_id = group[0].id

             techniques = attack_data.get_techniques_used_by_group(group_stix_id)
             if not techniques:
                  print(f"No ATT&CK Techniques associated with the threat group {selected_group_name}")
             else:
                  sort_phase(techniques)

def sort_phase(techniques):
    mitre_data = ""
    # Create a dictionary to store data by phase_name
    data_by_phase = {}
    for item in techniques:
        if 'object' in item and 'kill_chain_phases' in item['object'] and item['object']['kill_chain_phases']:
            # Extract the phase_name from the data
            phase_name = item['object']['kill_chain_phases'][0]['phase_name']
            
            # Check if the phase_name exists in the data_by_phase dictionary
            if phase_name not in data_by_phase:
                data_by_phase[phase_name] = []
            
            # Add the item to the list associated with the phase_name
            data_by_phase[phase_name].append(item)

    # Print the data grouped by phase_name
    for phase_name, items in data_by_phase.items():
        mitre_data += f"Phase Name: {phase_name}\n"
        #print(f"Phase Name: {phase_name}")
        for item in items:
            technique_object = item['object']
            technique_name = technique_object.get('name', 'N/A')
            technique_description = technique_object.get('description', 'N/A')
            external_references = technique_object.get('external_references', [])
            
            # Search for external_id within the external_references
            technique_external_id = 'N/A'
            for ref in external_references:
                if 'external_id' in ref:
                    technique_external_id = ref['external_id']
                    break
            mitre_data += f" Technique Name: {technique_name}\n"
            mitre_data += f" Technique External ID: {technique_external_id}\n"
            #print(f" Technique Name: {technique_name}")
            #print(f"  Technique Description: {technique_description}")
            #print(f" Technique External ID: {technique_external_id}")
    generate_text(mitre_data)

def generate_text(mitre_data):
    phase_name_order = [
        'Reconnaissance', 'Resource Development', 'Initial Access', 'Execution', 'Persistence', 
        'Privilege Escalation', 'Defense Evasion', 'Credential Access', 'Discovery', 'Lateral Movement', 
        'Collection', 'Command and Control', 'Exfiltration', 'Impact'
    ]

    industry = input("Enter your company's industry: ")
    comp_size = int(input("Enter company size (no commas): "))
    handrail = input("Would you like a assistance on how teams should action each scenario? [YES OR NO]".lower())
    if handrail == "yes":
        help = "Under each phase phase, please provide assistance and recommended actions for 1. The Cyber Analysts dealing with the incident and 2. The Cyber Threat Intelligence team"
    else:
        help = ""
    system_template = "You are a cybersecurity expert. Your task is to produce a comprehensive incident response testing scenario based on the information provided."
    human_template = f"""
                          **Background information:**
                          The company operates in the '{industry}' industry and is of size '{comp_size}'. 
                          
                          **Threat actor information:**
                          Threat actor group '{selected_group_name}' is planning to target the company using the following Tactics and Techniques:
                          {mitre_data}. Please order them in the killchain order of {phase_name_order}. You don't need to use all provided, as long as it creates a convincing incident simulation. 
                          
                          **Your task:**
                          Create an incident response testing scenario based on the information provided. The goal of the scenario is to test the company's incident 
                          response capabilities against the identified threat actor group. 
                          For Example: 
                          During this phase, the threat actors from the LAPSUS$ group actively engage in reconnaissance to gather credentials associated with the target organization. The objective is to obtain legitimate access credentials that can be potentially used for unauthorized access to the company's systems and resources.
                          Your response should be well structured and formatted using Markdown. Write in British English.
                          {help}
                          """
    result = system_template + '\n\n' + human_template
    print(result)


def load_attack_data():
    attack_data = MitreAttackData("enterprise-attack.json")
    return attack_data

def main():

    list_group()
  
if __name__ == "__main__":
    main()

 
