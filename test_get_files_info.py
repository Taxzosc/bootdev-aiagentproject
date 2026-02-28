from functions.get_files_info import get_file_info

print(get_file_info("calculator","."))
print(get_file_info("calculator", "pkg"))
print(get_file_info("calculator", "/bin"))
print(get_file_info("calculator", "../"))