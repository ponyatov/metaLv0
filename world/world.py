
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
import config
# / <section:top>
# \ <section:mid>


import sys, re, shapefile

json = 'location.json'

if sys.argv[1] == '[':
    with open(json, 'w') as j:
        j.write('''[
{
  "model": "app.location",
  "pk": 6,
  "fields": {
    "name": "Самара",
    "okato": "36401000000",
    "kladr": "6300000100000",
    "shape": "SRID=4326;POLYGON ((50.06063727990416 53.16853066866464, 50.08741645470595 53.20062492440238, 50.14852790489245 53.22899597916636, 50.16912727012365 53.24954297519994, 50.184920116801 53.27870276414777, 50.21650581015662 53.27788163379629, 50.25152473105017 53.25529436662115, 50.26937751425046 53.25940202997064, 50.27212409628135 53.25159713232568, 50.32362250936021 53.26925881262933, 50.36894111286935 53.25529436662115, 50.36276130329964 53.24420170509858, 50.34628181111523 53.23105112264669, 50.32018928182138 53.22324105261362, 50.31881599080639 53.19897964936175, 50.26525764120459 53.17470450626394, 50.22543220175631 53.17511606385209, 50.17256049766247 53.16482593968877, 50.13204841270715 53.17100031030591, 50.11213569298302 53.1714119034274, 50.0970294918136 53.17552761749165, 50.06063727990416 53.16853066866464))"
  }
},
{
  "model": "app.location",
  "pk": 7,
  "fields": {
    "name": "Тольятти",
    "shape": "SRID=4326;POLYGON ((49.21887895432563 53.59460427437186, 49.2065193351871 53.56076653546396, 49.25595781174212 53.55627998316078, 49.24153825608064 53.50199582468195, 49.29029008712862 53.48524757760645, 49.30402299728215 53.46726649000642, 49.35826799239189 53.47053634540902, 49.38161393965486 53.45827308872778, 49.4015266593781 53.46685774036894, 49.43997880781047 53.47176247624188, 49.47637101971992 53.46849271530215, 49.49147722088934 53.47217117864793, 49.50795671307463 53.49096723495284, 49.48873063885844 53.49423526429173, 49.50727006756669 53.52200334673357, 49.49147722088934 53.52812621008867, 49.48941728436639 53.56810714023414, 49.40289995039399 53.579930990661, 49.27793046798919 53.59338169530925, 49.21887895432563 53.59460427437186))"
  }
},
{
  "model": "app.location",
  "pk": 8,
  "fields": {
    "name": "Сызрань",
    "shape": "SRID=4326;POLYGON ((48.58177451765868 53.16048276560634, 48.5865810362125 53.16871589546119, 48.58246116316663 53.18065112850274, 48.57387809431955 53.177358982058, 48.56941489852015 53.18023962401516, 48.57765464461191 53.18291433261935, 48.57559470808897 53.18702894324687, 48.56838493025779 53.18867467696454, 48.56254844344249 53.18291433261935, 48.55602531111926 53.18085687926662, 48.55190543807338 53.18641177681909, 48.54297904647278 53.19176025744963, 48.5313060728413 53.19710807097069, 48.5299327818263 53.19299442747166, 48.50693015731776 53.19628537384902, 48.512079998626 53.20393585651745, 48.50830344833365 53.20969337702983, 48.49251060165629 53.20989898845529, 48.48701743759452 53.20619783183209, 48.49182395614834 53.19858889479049, 48.48289756454775 53.19714921420015, 48.47568778671656 53.18953867067205, 48.46676139511686 53.18645293031394, 48.46401481308597 53.18789297011399, 48.45165519394655 53.182955489471, 48.44890861191566 53.18768725310292, 48.41457633652826 53.18262630576582, 48.39809684434295 53.18715238613957, 48.37852744737324 53.19167798885704, 48.37097434678854 53.18180333074154, 48.38161735215855 53.17665937906359, 48.39294700303561 53.17110321837664, 48.40153007188268 53.16352921464205, 48.40736655869798 53.15467746670183, 48.42315940537534 53.15158921821944, 48.35483817735765 53.12304328813302, 48.35827140489558 53.05821939654361, 48.3733776060659 53.03427753080418, 48.39947013535885 53.02684459242138, 48.40084342637473 53.00123244257168, 48.4241893736368 52.97725892608979, 48.48324088730037 52.99544694996435, 48.44753532089887 53.05409243740887, 48.43242911972946 53.09781809501369, 48.49834708846979 53.13902801796289, 48.49216727890277 53.15994754995939, 48.53817252791896 53.16900401886292, 48.58177451765868 53.16048276560634))"
  }
},
{
  "model": "app.location",
  "pk": 9,
  "fields": {
    "name": "KUF",
    "okato":"36401373000",
    "kladr":"63000001000248100",
    "shape": "SRID=4326;POLYGON ((50.19024161948646 53.48344989369736, 50.18457679404748 53.48375633645192, 50.17307548179321 53.49764608326911, 50.16569404258571 53.4989735414687, 50.16895560874732 53.50305776756379, 50.16277579917761 53.50295566670707, 50.13204841270715 53.49305071472152, 50.129816814807 53.49417407302236, 50.1193454708151 53.49284646456083, 50.11488227501479 53.49825876144858, 50.11659888878421 53.50407876260974, 50.12449531212243 53.50775414116641, 50.13977317466907 53.51153128148796, 50.16105918540819 53.5194927988397, 50.17479209556351 53.52296273881717, 50.19195823325677 53.49213158436742, 50.19024161948646 53.48344989369736))"
  }
},
{
  "model": "app.location",
  "pk": 10,
  "fields": {
    "name": "Новодевичье",
    "shape": "SRID=4326;POLYGON ((48.85531759234853 53.61678801416038, 48.85840749713383 53.61200189200456, 48.85154104205618 53.60629856999844, 48.84415960284868 53.6036503372212, 48.84364461871795 53.60222429694571, 48.83952474567116 53.60079820852387, 48.83780813190175 53.60181684802418, 48.83282995197162 53.59957580869774, 48.83231496784088 53.59702902877692, 48.82373189899381 53.59672340486881, 48.81652212116263 53.59886272579634, 48.81875371906277 53.60161312208899, 48.8220152852244 53.6044651957621, 48.83454656574013 53.61037245003222, 48.8445029256022 53.61444593706542, 48.84982442828766 53.61454776920623, 48.85531759234853 53.61678801416038))"
  }
},
{
  "model": "app.location",
  "pk": 11,
  "fields": {
    "name": "Хворостянка",
    "shape": "SRID=4326;POLYGON ((48.93608427019291 52.63256357702814, 48.94878721208585 52.6321468332391, 48.96046018571734 52.61693296830224, 48.9793429371791 52.62339429672642, 48.98346281022588 52.61067916171795, 48.99341917008795 52.60609246916587, 48.97590970964118 52.59524928611384, 48.96011686296381 52.58565500208783, 48.95359373063967 52.59524928611384, 48.95050382585527 52.60108825666276, 48.93986082048615 52.60275639102343, 48.94329404802409 52.60838587549124, 48.92681455583878 52.62526998763241, 48.93608427019291 52.63256357702814))"
  }
},
{
  "model": "app.location",
  "pk": 12,
  "fields": {
    "name": "Б.Глушица",
    "shape": "SRID=4326;POLYGON ((50.48206663081558 52.42053468154991, 50.44395780513763 52.39267845094254, 50.46181058833792 52.36983579157641, 50.48618650386146 52.37318958253788, 50.51811551997061 52.37654311884749, 50.52051877924796 52.38513539334927, 50.49957609126236 52.39582101118412, 50.49408292720059 52.40545680063116, 50.48240995356911 52.40210546036774, 50.48206663081558 52.42053468154991))"
  }
},
{
  "model": "app.location",
  "pk": 13,
  "fields": {
    "name": "Б.Черниговка",
    "shape": "SRID=4326;POLYGON ((50.87826108877088 52.07121392090999, 50.89439725820176 52.08281929160788, 50.88581418935559 52.09906174219071, 50.87860441152439 52.10981647404792, 50.85972166006263 52.11023817539013, 50.85148191396998 52.10496662193775, 50.82676267569202 52.10117071755965, 50.83259916250731 52.09167954309594, 50.84392881338438 52.09421072040299, 50.85594510977027 52.08176438257966, 50.87139463369321 52.07817750537912, 50.87826108877088 52.07121392090999))"
  }
},
{
  "model": "app.location",
  "pk": 14,
  "fields": {
    "name": "К.Черкассы",
    "okato": "36220832001",
    "kladr": "6301100000100",
    "shape": "SRID=4326;POLYGON ((51.46280562814126 53.45182402701436, 51.45765578683302 53.46408914632242, 51.44769942697095 53.46572422789325, 51.44872939523241 53.48043712816178, 51.45662581857155 53.48207158000405, 51.45799910958654 53.48840448616102, 51.48992812569568 53.48391026306141, 51.50091445381922 53.49228547746953, 51.51842391426599 53.48574886642847, 51.53353011543541 53.48268448321114, 51.53181350166599 53.47635072306878, 51.55069625312866 53.47349000533284, 51.56271254951367 53.47859829457303, 51.57266890937573 53.47798533233291, 51.56442916328309 53.45550393480289, 51.55069625312866 53.45673049987463, 51.53833663399013 53.45182402701436, 51.54142653877454 53.4479393339668, 51.53593337471277 53.44507670121035, 51.52426040108129 53.45039286564845, 51.50709426338894 53.43710120701344, 51.49851119454186 53.44016888195316, 51.49542128975745 53.44425877070496, 51.48512160714186 53.4469169872704, 51.48512160714186 53.45366402076686, 51.46280562814126 53.45182402701436))",
    "userbind": false
  }
},
{
  "model": "app.location",
  "pk": 15,
  "fields": {
    "name": "Клявлино",
    "okato": "36222824001",
    "kladr": "6301300000100",
    "shape": "SRID=4326;POLYGON ((52.03014647889114 54.27816110494977, 52.03872954773822 54.27445262729854, 52.04130446839189 54.269941866838, 52.03958785462248 54.26563112333619, 52.03529632019939 54.26312466986786, 52.04250609803057 54.25931456873381, 52.03752791809953 54.25710855977661, 52.04216277527615 54.25410017554495, 52.03684127259159 54.247581256802, 52.02825820374542 54.24848393777402, 52.02877318787615 54.24547492438066, 52.02173507142218 54.24477278967348, 52.02070510316072 54.24728035875498, 52.0174435369991 54.24728035875498, 52.00680053162908 54.24547492438066, 52.00611388612113 54.24748095769669, 52.00989043641349 54.25069040810242, 52.00920379090644 54.25821157900787, 51.99941909242069 54.26051779660405, 52.00062072205937 54.26482907480619, 52.00594222474483 54.2638264921999, 52.00937545228275 54.2666336620541, 52.00508391785966 54.27024259956161, 52.0100620977907 54.27174623026588, 52.00971877503717 54.27615656388015, 52.01641356873672 54.27735930022381, 52.02001845765277 54.27395145607203, 52.03014647889114 54.27816110494977))",
    "userbind": false
  }
},
{
  "model": "app.location",
  "pk": 16,
  "fields": {
    "name": "Ч.Вершины",
    "okato": "36246832001",
    "kladr": "6302500000100",
    "shape": "SRID=4326;POLYGON ((51.06970107497307 54.43890745606321, 51.06334960402705 54.43790911164417, 51.05991637648822 54.42912263150982, 51.06334960402705 54.42472868476725, 51.05648314894939 54.42552761921876, 51.05304992141055 54.42013450941192, 51.05785643996528 54.41484058191636, 51.06695449294219 54.41034520114053, 51.08858382643484 54.40255204017049, 51.09167373122015 54.39715590731831, 51.09939849318206 54.39685610134598, 51.10266005934368 54.40355124613413, 51.10952651442045 54.40854691082166, 51.10557830275089 54.41484058191636, 51.11398971022074 54.41573959892651, 51.11141478956708 54.4202343882647, 51.10094344557427 54.42013450941192, 51.09133040846572 54.43251763130996, 51.07948577345793 54.43271732841998, 51.06970107497307 54.43890745606321))",
    "userbind": false
  }
},
''')
    sys.exit(0)

if sys.argv[1] == ']':
    with open(json, 'a') as a:
        a.seek(0, 2)
        a.truncate(a.tell() - 1)
        a.write("\n]\n")
    sys.exit(0)

nameshp = sys.argv[1]
assert re.match(r'^[A-Z][a-z]+\.shp$', nameshp)
pk = sys.argv[2]
assert re.match(r'\d+', pk)
areaname = sys.argv[3]
assert re.match(r'^.+ область$', areaname)
okato = sys.argv[4]
assert re.match(r'^((36|53)\d{9}|)$', okato)
okato = f'"{okato}"' if okato else 'null'
kladr = sys.argv[5]
assert re.match(r'^((63|56)\d{11,15}|)$', kladr)
kladr = f'"{kladr}"' if kladr else 'null'

with open(json, 'a') as j:
    with shapefile.Reader(nameshp) as shp:
        print(f'shp: {nameshp}')
        feature = shp.shapeRecords()[0]
        print(f'feature: {feature}')
        first = feature.shape.__geo_interface__
        dat = first['coordinates'][0]
        dat = ', '.join(f'{i[0]} {i[1]}' for i in dat)
        dat = dat
        j.write(f"""
{{
	"model": "app.location",
	"pk": {pk},
	"fields": {{
		"name":  "{areaname}",
    "okato": {okato},
    "kladr": {kladr},
    "userbind": true,
    "shape": "SRID=4326;POLYGON (({dat}))"
	}}
}},""")


# / <section:mid>