import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

def format_time(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}.{int((seconds % 1) * 100):02d}"

def format_txt(result):
    output = f"Detected language: {result['language']}\n\n"
    for segment in result['segments']:
        if segment['type'] == 'pause':
            output += f"[{format_time(segment['start'])} -> {format_time(segment['end'])}] PAUSE\n\n"
        else:
            output += f"[{format_time(segment['start'])} -> {format_time(segment['end'])}] {segment['speaker']}\n {segment['text']}\n\n"
    
    if result['translation']:
        output += f"\nTranslation:\n{result['translation']}\n"
    
    return output

def format_json(result):
    return json.dumps(result, indent=2, ensure_ascii=False)

def format_csv(result):
    output = []
    writer = csv.writer(output)
    writer.writerow(['Type', 'Start', 'End', 'Speaker', 'Text'])
    for segment in result['segments']:
        writer.writerow([
            segment['type'],
            format_time(segment['start']),
            format_time(segment['end']),
            segment.get('speaker', ''),
            segment.get('text', '')
        ])
    return ''.join(output)

def format_xml(result):
    root = ET.Element('transcript')
    ET.SubElement(root, 'language').text = result['language']
    segments = ET.SubElement(root, 'segments')
    for segment in result['segments']:
        seg = ET.SubElement(segments, 'segment')
        ET.SubElement(seg, 'type').text = segment['type']
        ET.SubElement(seg, 'start').text = format_time(segment['start'])
        ET.SubElement(seg, 'end').text = format_time(segment['end'])
        if 'speaker' in segment:
            ET.SubElement(seg, 'speaker').text = segment['speaker']
        if 'text' in segment:
            ET.SubElement(seg, 'text').text = segment['text']
    if result['translation']:
        ET.SubElement(root, 'translation').text = result['translation']
    
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    return xml_str

formatters = {
    'txt': format_txt,
    'json': format_json,
    'csv': format_csv,
    'xml': format_xml
}