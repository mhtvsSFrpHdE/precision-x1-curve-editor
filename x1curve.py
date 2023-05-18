import os
import pathlib
import xml.etree.ElementTree as ET

# Which profile to modify
targetProfile = 0
# Set one of available clock speed from nvidia-smi
# You may want to signtly lower two available level
# My card final frequency may higher than I thought (not always)
# For example, if want 1012 but get 1037, then set 987 to get 1012
targetClock = 708
# Set to true when underclock curve is available
# When set to False, points before targetClock will be set to 0
# In case you don't want to try underclock
enableUnderclock = False
# When first point is dragged to bottom, it's value in MHz
minClock = 215
#
#
#
# PRECISION X1 config file
versionFolder = os.getenv('LOCALAPPDATA') + r"\EVGA_Co.,_Ltd\PrecisionX_x64.exe_Url_vrvasebqwl5wesi2q3tshmshuzsvqfah"
# Get latest modified version folder
versionFolder = max(pathlib.Path(versionFolder).glob('*/'), key=os.path.getmtime)
configFileName = versionFolder.joinpath("user.config")
# Drag all points to zero, copy <offsets>...</offsets> from profile and paste to new file
# So the file contains maximum frequency per voltage information of your card
defaultCurveFileName = "Curve\\DefaultCurve.xml"
# PRECISION X1 overclock scan result
underclockFileName = "Curve\\UnderclockCurve.xml"
# Usually same as "PRECISION X1 config file"
# The code is relatively stable now
saveTo = configFileName

# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


parsedConfig = ET.parse(configFileName)
parsedDefaultCurve = ET.parse(defaultCurveFileName)
parsedUnderclockCurve = ET.parse(underclockFileName) if enableUnderclock else None
configuration = parsedConfig.getroot()
defaultCurve = parsedDefaultCurve.getroot()
underclockCurve = parsedUnderclockCurve.getroot() if enableUnderclock else None


GpuProfiles = configuration.findall("./userSettings/PX18.Properties.Settings/setting[@name='VgaProfiles']/value/VgaProfiles/Items/*")
minimumVfPoints = defaultCurve.findall("./*")
underclockedVfPoints = underclockCurve.findall("./*") if enableUnderclock else None

notNegativeResult = False
for GpuProfile in GpuProfiles:
    profileIndex = int(GpuProfile.find('index').text)
    # Modify target profile
    if profileIndex == targetProfile:
        offsetItemLists = GpuProfile.findall('./Items/GpuProfile/AutoScanResult/offsets/*')

        for index, offsetItem in enumerate(offsetItemLists):
            offsetFrequencyKhz = offsetItem.find('offsetFrequencyKhz')
            minimumOffsetFrequencyKhz = minimumVfPoints[index].find('offsetFrequencyKhz')
            underclockedOffsetFrequencyKhz = underclockedVfPoints[index].find('offsetFrequencyKhz') if enableUnderclock else None

            print(str(index + 1) + ' Before: ' + offsetFrequencyKhz.text)

            absoluteFreq = (minClock * 1000) + abs(int(minimumOffsetFrequencyKhz.text)) + ((int(underclockedOffsetFrequencyKhz.text)) if enableUnderclock else 0)
            if absoluteFreq <= targetClock * 1000:
                if enableUnderclock:
                    offsetFrequencyKhz.text = underclockedOffsetFrequencyKhz.text
                    print(str(index + 1) + ' After: ' + offsetFrequencyKhz.text)
                    continue
                else:
                    offsetFrequencyKhz.text = '0'
                    print(str(index + 1) + ' After: ' + offsetFrequencyKhz.text)
                    continue

            offsetValue = (targetClock * 1000) + (int(underclockedOffsetFrequencyKhz.text) if enableUnderclock else 0) - absoluteFreq
            if offsetValue > 0:
                notNegativeResult = True
                print(f"{bcolors.WARNING}Warning: Value greater than zero{bcolors.ENDC}")
            offsetFrequencyKhz.text = str(offsetValue)

            print(str(index + 1) + ' After: ' + offsetFrequencyKhz.text)

    # After reboot, X1 treat offset of 708 as offset of 721 or 749 for unknown readon
    # But load profile 9 (DefaultCurve.xml), close X1, open X1, load profile 0 seems fixed this
    # Reset startup profile to emulate such behavior to fix curve distortion
    # 4294967295 in X1 config means "last time used profile"
    if profileIndex == 4294967295:
        offsetItemLists = GpuProfile.findall('./Items/GpuProfile/AutoScanResult/offsets/*')

        for index, offsetItem in enumerate(offsetItemLists):
            offsetFrequencyKhz = offsetItem.find('offsetFrequencyKhz')
            minimumOffsetFrequencyKhz = minimumVfPoints[index].find('offsetFrequencyKhz')
            offsetFrequencyKhz.text = minimumOffsetFrequencyKhz.text


if notNegativeResult:
    print(f"{bcolors.WARNING}Warning: One or more value great than zero and may cause your card to burn if too much{bcolors.ENDC}")
parsedConfig.write(saveTo)
