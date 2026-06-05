[Setup]
AppName = ORION
AppVersion=1.00
DefaultDirName={autopf}\ORION
OutputDir=installer
OutputBaseFilename=ORION_Setup_1.0.0
SetupIconFile==C:\Users\ague_\Desktop\programacion\macondo_hackclub\ORION\assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Iconos adicionales:"
Name: "startupicon"; Description: "Iniciar ORION con Windows"; GroupDescription: "Inicio automático:"

[Files]
Source: "C:\Users\ague_\Desktop\programacion\macondo_hackclub\ORION\dist\app.exe"; DestDir: "{app}"; DestName: "ORION.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\ORION"; Filename: "{app}\ORION.exe"
Name: "{userdesktop}\ORION"; Filename: "{app}\ORION.exe"; Tasks: desktopicon
Name: "{userstartup}\ORION"; Filename: "{app}\ORION.exe"; Tasks: startupicon

[Run]
Filename: "{app}\ORION.exe"; Description: "Lanzar ORION"; Flags: nowait postinstall skipifsilent