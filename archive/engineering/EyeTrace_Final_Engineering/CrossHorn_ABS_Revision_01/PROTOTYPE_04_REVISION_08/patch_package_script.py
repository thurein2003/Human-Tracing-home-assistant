from pathlib import Path
p=Path(r'EyeTrace_Final_Engineering\CrossHorn_ABS_Revision_01\PROTOTYPE_04_REVISION_08\package_prototype_04_revision_08_3mf.py')
s=p.read_bytes().decode('utf-8').lstrip('\ufeffï»¿')
s=s.replace("obj.attrib['name']='Ultra-minimal ABS cross-horn fit gauge - Prototype 04 Revision 04'", "obj.attrib['name']='Ultra-minimal ABS cross-horn fit gauge - Prototype 04 Revision 08'")
s=s.replace("for x,y,z in vs: ET.SubElement(vr,tag('vertex'),{'x':str(x),'y':str(y),'z':str(z)})", "# Bed-based project coordinates: center the STL mesh on the 260 mm K2 plate.\nfor x,y,z in vs: ET.SubElement(vr,tag('vertex'),{'x':str(x+130.0),'y':str(y+130.0),'z':str(z)})")
s=s.replace("if e.attrib.get('key')=='name': e.attrib['value']='Ultra-minimal cross-horn gauge 04R08'", "if e.attrib.get('key')=='name': e.attrib['value']='Ultra-minimal cross-horn gauge 04R08'\n    if e.attrib.get('key')=='sparse_infill_density': e.attrib['value']='0%'")
p.write_text(s,encoding='utf-8')
