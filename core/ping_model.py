import asyncio
import platform
import subprocess

class PingModel:
    async def ping_host(self, ip: str) -> dict:
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        startupinfo = None
        if platform.system().lower() == 'windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        try:
            process = await asyncio.create_subprocess_exec(
                'ping', param, '1', '-w', '1000', ip,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                startupinfo=startupinfo
            )

            await process.wait()
            is_alive = process.returncode == 0
            return {"ip": ip, "status": "Online" if is_alive else "Offline"}

        except Exception as e:
            return {"ip": ip, "status": "Error"}

    async def ping_many(self, targets: list) -> list:
        tasks = [self.ping_host(ip) for ip in targets]
        return await asyncio.gather(*tasks)