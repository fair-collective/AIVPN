// aivpn/ui/lib/main.dart
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(AIVPNApp());

class AIVPNApp extends StatefulWidget {
  @override _AIVPNAppState createState() => _AIVPNAppState();
}

class _AIVPNAppState extends State<AIVPNApp> {
  final SpeechToText _speech = SpeechToText();
  String _text = "Say: 'AIVPN, find The Office'";
  List<Map<String, String>> _recs = [];

  @override
  void initState() {
    super.initState();
    _initSpeech();
  }

  void _initSpeech() async {
    await _speech.initialize();
  }

  void _listen() async {
    if (!_speech.isListening) {
      await _speech.listen(onResult: (result) {
        setState(() => _text = result.recognizedWords);
        if (result.finalResult) _search(result.recognizedWords);
      });
    }
  }

  void _search(String query) async {
    if (!query.toLowerCase().contains("aivpn")) return;
    final title = query.split("find")[1].trim();
    
    final res = await http.post(
      Uri.parse("https://adam.ceo/aivpn/search"),
      body: json.encode({"title": title})
    );
    final data = json.decode(res.body);
    setState(() => _recs = List<Map<String, String>>.from(data["recommendations"]));
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(title: Text("AIVPN", style: TextStyle(color: Colors.cyan))),
        body: Column(
          children: [
            Padding(
              padding: EdgeInsets.all(20),
              child: Text(_text, style: TextStyle(color: Colors.cyan, fontSize: 18)),
            ),
            ElevatedButton(
              onPressed: _listen,
              child: Icon(_speech.isListening ? Icons.mic : Icons.mic_off),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: _recs.length,
                itemBuilder: (c, i) {
                  final r = _recs[i];
                  return Card(
                    color: r["type"] == "free" ? Colors.green[900] : Colors.purple[900],
                    child: ListTile(
                      title: Text(r["message"]!, style: TextStyle(color: Colors.white)),
                      trailing: r["type"] == "free" 
                        ? Icon(Icons.play_arrow, color: Colors.white)
                        : Icon(Icons.attach_money, color: Colors.yellow),
                      onTap: () => _connect(r),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _connect(Map<String, String> r) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Connecting to ${r['country'] ?? r['company']}..."))
    );
  }
}
