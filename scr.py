import re
from http.client import responses


def requestparser(line):

    method_match = re.search(r"(GET|POST|HEAD|PUT|OPTIONS|DELETE|UPDATE|PATCH)", line)
    method = method_match.group(1)
    request_source_match = re.search(r"(localhost:)(\d+)", line)
    request_source = request_source_match.group(1)
    request_source_port = request_source_match.group(2)
    status_match = re.search(r"\=(\d{3})", line)
    try:
        status = int(status_match.group(1))
        try:
            status_check = responses[status]
            status = status
        except KeyError:
            status = 200
        http_response_wstatus = [
            f"HTTP/1.0 {status} {responses[status]}",
            f"Request Method: {method}",
            f"Request Source: ('{request_source}', {request_source_port})",
            f"Response Status: {status} {responses[status]}"
        ]
        line_m = line.splitlines()
        if '' in line_m:
            line_m.remove('')
        line_2 = line_m[2:-1]
        http_response_wstatus.extend(line_2)
        nl = []
        for i in http_response_wstatus:
            nl.append(f'{i}\r\n')
        st = ''
        for i in nl:
            st += nl[nl.index(i)]
        the_end = "\r\n"
        st += the_end
        return st

    except AttributeError:
        http_response = [
            f"HTTP/1.0 200 OK",
            f"Request Method: {method}",
            f"Request Source: ('{request_source}', {request_source_port})"
        ]
        line_m = line.splitlines()
        if '' in line_m:
            line_m.remove('')
        line_2 = line_m[2:]
        http_response.extend(line_2)
        nl = []
        for i in http_response:
            nl.append(f'{i}\r\n')
        st = ''
        for i in nl:
            st += nl[nl.index(i)]
        the_end = "\r\n"
        st += the_end
        return st


