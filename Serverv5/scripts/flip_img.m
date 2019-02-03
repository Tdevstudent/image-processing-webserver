function test(image_inpath, json_path, image_outpath)
% print JSON to console
jsondecode(fileread(json_path));
% copyfile(image_inpath, image_outpath);
imwrite(imrotate(imread(image_inpath), 180), image_outpath);
