function init (args)
    local needs = {}
    needs["packet"] = tostring(true)
    return needs
end

function match(args)
    a = tostring(args["packet"])
    if #a > 0 then
			if math.random() < 0.65 then
          return 1
        end
    end

    return 0
end

return 0











