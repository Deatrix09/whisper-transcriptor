import json
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

def format_txt(segments):
    output = ""
    for segment in segments:
        output += f"[{segment['start']:.1f}s -> {segment['end']:.1f}s]\n"
        output += f"Transcript: {segment['transcript']}\n"
        if segment['translation']:
            output += f"Translation: {segment['translation']}\n"
        if segment['diarization']:
            for start, end, speaker in segment['diarization']:
                output += f"  [{start:.1f}s -> {end:.1f}s] Speaker {speaker}\n"
        output += "\n"
    return output

def format_json(segments):
    return json.dumps(segments, indent=2)

def format_csv(segments):
    output = []
    output.append(['start', 'end', 'transcript', 'translation', 'speaker'])
    for segment in segments:
        if segment['diarization']:
            for start, end, speaker in segment['diarization']:
                output.append([start, end, segment['transcript'], segment['translation'], speaker])
        else:
            output.append([segment['start'], segment['end'], segment['transcript'], segment['translation'], ''])
    
    csv_output = []
    writer = csv.writer(csv_output)
    writer.writerows(output)
    return ''.join(csv_output)

def format_xml(segments):
    root = ET.Element("transcript")
    
    for segment in segments:
        seg = ET.SubElement(root, "segment")
        ET.SubElement(seg, "start").text = str(segment['start'])
        ET.SubElement(seg, "end").text = str(segment['end'])
        ET.SubElement(seg, "transcript").text = segment['transcript']
        if segment['translation']:
            ET.SubElement(seg, "translation").text = segment['translation']
        if segment['diarization']:
            diarization = ET.SubElement(seg, "diarization")
            for start, end, speaker in segment['diarization']:
                turn = ET.SubElement(diarization, "turn")
                ET.SubElement(turn, "start").text = str(start)
                ET.SubElement(turn, "end").text = str(end)
                ET.SubElement(turn, "speaker").text = speaker
    
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    return xml_str

formatters = {
    'txt': format_txt,
    'json': format_json,
    'csv': format_csv,
    'xml': format_xml
}