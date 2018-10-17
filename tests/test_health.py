# utf-8
import os
import requests

from tests.get_access_token import GetAccessToken

# Health check API calls domain:
API_ROOT = os.getenv('API_ROOT', "https://acc.api.data.amsterdam.nl")

# Authentication flow domain, True => acceptance, False => production
AUTH_ACCEPTANCE = os.getenv('AUTH_ACCEPTANCE', True)

SCOPES = [
    "BRK/RS",
    "BRK/RSN",
    "BRK/RO",
    "WKPB/RBDU",
    "MON/RBC",
    "MON/RDM",
    "HR/R",
    "GREX/R",
    "CAT/W"
]


def setup_module():
    global auth_headers
    user = os.getenv('USERNAME_EMPLOYEE_PLUS')
    password = os.getenv('PASSWORD_EMPLOYEE_PLUS')

    if not user:
        raise Exception('USERNAME_EMPLOYEE_PLUS not provided!')
    if not password:
        raise Exception('PASSWORD_EMPLOYEE_PLUS not provided!')

    auth_headers = GetAccessToken().getAccessToken(user, password, SCOPES, AUTH_ACCEPTANCE)


def check_api_call(uri, do_authenticate=False):
    url = f"{API_ROOT}{uri}"

    if do_authenticate:
        response = requests.get(url, headers=auth_headers)
    else:
        response = requests.get(url)
    assert response.status_code == 200
    assert response.ok


def test_dcat():
    check_api_call("/dcatd/openapi")


def test_panorama():
    check_api_call("/dcatd/openapi")
    check_api_call("/panorama/recente_opnames/alle/TMX7316010203-000719_pano_0000_000950/")
    check_api_call("/panorama/thumbnail/?lat=52.375764&lon=4.8914344&width=438&radius=180")
    check_api_call("/panorama/thumbnail/?lat=52.375764&lon=4.8914344&width=240&radius=50")
    check_api_call("/panorama/thumbnail/TMX7316010203-000227_pano_0000_001568/?width=240&heading=156")


def test_typeahead():
    check_api_call("/typeahead?q=")


def test_dataselectie():
    check_api_call("/dataselectie/bag/?buurt_naam=AMC&dataset=ves&page=1&postcode=1105AZ&shape=%5B%5D", True)
    check_api_call("/dataselectie/hr/?bijzondere_rechtstoestand=Faillissement&buurt_naam=Amstel+III+deel+A%2FB+Noord&buurtcombinatie_naam=Amstel+III%2FBullewijk&dataset=ves&page=1&shape=%5B%5D", True)
    check_api_call("/dataselectie/brk/?buurt_naam=Amstelveldbuurt&dataset=ves&eigenaar_cat=Woningbouwcorporaties&eigenaar_type=Appartementseigenaar&ggw_naam=Centrum-Oost&page=1&shape=%5B%5D&stadsdeel_naam=Centrum", True)


def test_geosearch():
    check_api_call("/geosearch/nap/?lat=52.375764&lon=4.8914344&radius=25")
    check_api_call("/geosearch/atlas/?lat=52.375764&lon=4.8914344")
    check_api_call("/geosearch/munitie/?lat=52.375764&lon=4.8914344")
    check_api_call("/geosearch/bominslag/?lat=52.375764&lon=4.8914344&radius=25")
    check_api_call("/geosearch/monumenten/?lat=52.375764&lon=4.8914344&monumenttype=isnot_pand_bouwblok&radius=25")
    check_api_call("/geosearch/grondexploitatie/?lat=52.375764&lon=4.8914344")
    check_api_call("/geosearch/biz/?lat=52.375764&lon=4.8914344")


def test_grondexploitatie():
    check_api_call("/grondexploitatie/stadsdeel/A/", True)


def test_bag():
    check_api_call("/bag/nummeraanduiding/?pand=0363100012180422")
    check_api_call("/bag/pand/0363100012180422/")


def test_handelsregister():
    check_api_call("/handelsregister/vestiging/?pand=0363100012180422", True)


def test_monumenten():
    check_api_call("/monumenten/monumenten/?betreft_pand=0363100012180422")
    check_api_call("/monumenten/situeringen/?betreft_nummeraanduiding=0363200000268416")


def test_bbga():
    check_api_call("/bbga/cijfers/?gebiedcode15=A&jaar=latest&variabele=BEVHHMKIND_P")
    check_api_call("/bbga/meta/?variabele=BEVHHMKIND_P")


def test_gebieden():
    check_api_call("/gebieden/stadsdeel/03630000000018/")
    check_api_call("/gebieden/buurtcombinatie/?stadsdeel=03630000000018")


def test_brk():
    check_api_call("/brk/object-expand/?verblijfsobjecten__id=0363010000809818", True)
    check_api_call("/brk/subject/NL.KAD.Persoon.183189110/", True)
    check_api_call("/brk/zakelijk-recht/?kadastraal_subject=NL.KAD.Persoon.183189110", True)


def test_wkpb():
    check_api_call("/wkpb/brondocument/?beperking=3488")
    check_api_call("/wkpb/beperking/3488/")

def test_meetbouten():
    check_api_call("/meetbouten/meetbout")
    check_api_call("/meetbouten/meetbout/10581111/")
    check_api_call("/meetbouten/rollaag/1/")
