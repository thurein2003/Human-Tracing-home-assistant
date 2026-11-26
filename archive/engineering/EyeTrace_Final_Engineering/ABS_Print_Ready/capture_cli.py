import ctypes,subprocess,sys,json
from ctypes import wintypes as W
from pathlib import Path
r=Path(__file__).resolve().parent
class COORD(ctypes.Structure):_fields_=[('X',W.SHORT),('Y',W.SHORT)]
class RECT(ctypes.Structure):_fields_=[('Left',W.SHORT),('Top',W.SHORT),('Right',W.SHORT),('Bottom',W.SHORT)]
class INFO(ctypes.Structure):_fields_=[('size',COORD),('cursor',COORD),('attributes',W.WORD),('window',RECT),('maxsize',COORD)]
k=ctypes.windll.kernel32;k.AllocConsole();ctypes.windll.user32.ShowWindow(k.GetConsoleWindow(),0)
k.CreateFileW.restype=W.HANDLE;h=k.CreateFileW('CONOUT$',0xC0000000,3,None,3,0,None)
args=['D:\\Creality Print 7.2\\CrealityPrint.exe']+sys.argv[2:]
p=subprocess.run(args,cwd=str(r),stdin=subprocess.DEVNULL,timeout=600)
i=INFO();k.GetConsoleScreenBufferInfo(W.HANDLE(h),ctypes.byref(i));n=i.size.X*i.size.Y;buf=ctypes.create_unicode_buffer(n+1);read=W.DWORD();k.ReadConsoleOutputCharacterW(W.HANDLE(h),buf,n,COORD(0,0),ctypes.byref(read));s=buf.value
lines=[s[a:a+i.size.X].rstrip() for a in range(0,len(s),max(i.size.X,1))];out='\n'.join(v for v in lines if v.strip());(r/'CHECKS'/sys.argv[1]).write_text(out,encoding='utf-8');k.FreeConsole()
print(json.dumps({'exit_code':p.returncode,'console_file':sys.argv[1],'console_chars':len(out),'args':args},ensure_ascii=False))
