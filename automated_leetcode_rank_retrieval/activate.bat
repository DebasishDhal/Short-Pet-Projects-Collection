::First, we set up the virtual environment in which the script will run. Then we run the python script
set original_dir=%CD%
set venv_root_dir=C:\Users\HP\anaconda3
cd %venv_root_dir%
call %venv_root_dir%\Scripts\activate.bat

python C:\Users\HP\OneDrive\Desktop\Python\Pet_Projects\leetcode_rank_retrieval\script.py

call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%
exit /B 1
